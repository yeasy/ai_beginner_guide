from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github/workflows"
WORKFLOWS = tuple(sorted((*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml"))))
BUILD_WORKFLOWS = (
    ROOT / ".github/workflows/ci.yaml",
    ROOT / ".github/workflows/auto-release.yml",
)
MDPRESS_WORKFLOWS = BUILD_WORKFLOWS + (ROOT / ".github/workflows/preview-pdf.yml",)
VERIFIER = ROOT / "tools/verify_artifacts.py"
# 允许出现在 workflow 里的第三方 action。版本不写死——见下方跨文件一致性断言。
ALLOWED_ACTIONS = frozenset(
    {
        "actions/checkout",
        "actions/download-artifact",
        "actions/upload-artifact",
        "browser-actions/setup-chrome",
        "dependabot/fetch-metadata",
        "softprops/action-gh-release",
    }
)
TEST_REPOSITORY = "owner/repo"
TEST_SHA = "a" * 40
GET_REF_COMMAND = [
    "api",
    "--include",
    "--method",
    "GET",
    f"repos/{TEST_REPOSITORY}/git/ref/tags/preview-pdf",
]
PATCH_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "PATCH",
    f"repos/{TEST_REPOSITORY}/git/refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
    "--field",
    "force=true",
]
POST_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "POST",
    f"repos/{TEST_REPOSITORY}/git/refs",
    "--raw-field",
    "ref=refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
]
EDIT_RELEASE_COMMAND = [
    "release",
    "edit",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
]
VIEW_RELEASE_COMMAND = ["release", "view", "preview-pdf"]
CREATE_RELEASE_COMMAND = [
    "release",
    "create",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
    "--latest=false",
    "--verify-tag",
]

FAKE_GH = r'''#!/usr/bin/env python3
import json
import os
import sys

args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\n")

scenario = os.environ["GH_SCENARIO"]
repository = "owner/repo"
sha = "a" * 40
reasons = {
    "401": "Unauthorized",
    "403": "Forbidden",
    "404": "Not Found",
    "429": "Too Many Requests",
    "503": "Service Unavailable",
}

def fail_http(code):
    print(f"HTTP/2.0 {code} {reasons[code]}")
    print(f"fake gh HTTP {code}", file=sys.stderr)
    raise SystemExit(1)

get_ref = ["api", "--include", "--method", "GET", f"repos/{repository}/git/ref/tags/preview-pdf"]
patch_ref = [
    "api", "--silent", "--method", "PATCH",
    f"repos/{repository}/git/refs/tags/preview-pdf",
    "--raw-field", f"sha={sha}", "--field", "force=true",
]
post_ref = [
    "api", "--silent", "--method", "POST", f"repos/{repository}/git/refs",
    "--raw-field", "ref=refs/tags/preview-pdf", "--raw-field", f"sha={sha}",
]
edit_release = [
    "release", "edit", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
]
create_release = [
    "release", "create", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
    "--latest=false", "--verify-tag",
]
view_release = ["release", "view", "preview-pdf"]

if os.environ.get("GH_REPO") != repository:
    print("fake gh requires explicit GH_REPO", file=sys.stderr)
    raise SystemExit(2)

if args == get_ref:
    if scenario.startswith("ref_network"):
        print("fake gh network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if scenario.startswith(f"ref_{code}"):
            fail_http(code)
    print("HTTP/2.0 200 OK")
    print('Content-Type: application/json\n\n{"ref":"refs/tags/preview-pdf"}')
    raise SystemExit(0)

if args in (patch_ref, post_ref, edit_release, create_release):
    raise SystemExit(0)

if args == view_release:
    if "release_missing" in scenario:
        print("release not found", file=sys.stderr)
        raise SystemExit(1)
    if "release_network" in scenario:
        print("fake release network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if f"release_{code}" in scenario:
            print(f"fake release HTTP {code}", file=sys.stderr)
            raise SystemExit(1)
    raise SystemExit(0)

print(f"unexpected gh argv: {args!r}", file=sys.stderr)
raise SystemExit(2)
'''


def workflow_step_script(workflow_text, step_name):
    marker = f"      - name: {step_name}\n"
    start = workflow_text.index(marker) + len(marker)
    run_marker = "        run: |\n"
    script_start = workflow_text.index(run_marker, start) + len(run_marker)
    script_end = workflow_text.find("\n      - name:", script_start)
    if script_end < 0:
        script_end = len(workflow_text)
    return textwrap.dedent(workflow_text[script_start:script_end])


def workflow_step_scripts_in_document_order(workflow_text, step_names):
    ordered_names = sorted(
        step_names,
        key=lambda name: workflow_text.index(f"      - name: {name}\n"),
    )
    return tuple(workflow_step_script(workflow_text, name) for name in ordered_names)


def load_verifier():
    if not VERIFIER.exists():
        raise AssertionError("tools/verify_artifacts.py must exist")
    spec = importlib.util.spec_from_file_location("verify_artifacts", VERIFIER)
    if spec is None or spec.loader is None:
        raise AssertionError("tools/verify_artifacts.py must be importable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def job_block(workflow_text: str, job_name: str) -> str:
    match = re.search(
        rf"(?ms)^  {re.escape(job_name)}:\n.*?(?=^  [A-Za-z0-9_-]+:\n|\Z)",
        workflow_text,
    )
    if match is None:
        raise AssertionError(f"workflow must define the {job_name!r} job")
    return match.group(0)


class WorkflowSafetyTests(unittest.TestCase):
    def test_mermaid_dependency_is_exact_and_lockfile_backed(self) -> None:
        package = json.loads((ROOT / "tools/mermaid/package.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "tools/mermaid/package-lock.json").read_text(encoding="utf-8"))
        dependency = "@mermaid-js/mermaid-cli"
        pinned = package["dependencies"][dependency]
        self.assertIsNotNone(
            re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", pinned),
            "mermaid-cli must be pinned to an exact version",
        )
        self.assertGreaterEqual(lock["lockfileVersion"], 3)
        self.assertEqual(
            lock["packages"][""]["dependencies"][dependency],
            pinned,
            "lockfile root dependency must match package.json",
        )
        self.assertEqual(
            lock["packages"][f"node_modules/{dependency}"]["version"],
            pinned,
            "resolved mermaid-cli version must match package.json",
        )

    def test_mdpress_is_extracted_to_an_isolated_directory(self) -> None:
        for workflow in MDPRESS_WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertNotRegex(
                    text,
                    r'(?m)^\s*tar\s+xzf\s+"\$archive"\s*$',
                    "extracting the full mdPress archive in the repository root overwrites README.md",
                )
                self.assertIn('extract_dir="$(mktemp -d)"', text)
                self.assertRegex(
                    text,
                    r'tar\s+--extract\s+--gzip\s+--file\s+"\$archive"\s+'
                    r'--directory\s+"\$extract_dir"\s+mdpress',
                )

    def test_third_party_actions_are_pinned_and_checkout_drops_credentials(self) -> None:
        self.assertEqual(
            {workflow.name for workflow in WORKFLOWS},
            {
                "auto-release.yml",
                "ci.yaml",
                "dependabot-automerge.yml",
                "identity-guard.yaml",
                "preview-pdf.yml",
            },
        )
        observed: dict[str, set[tuple[str, str]]] = {}
        for workflow in WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                uses_lines = [line.strip() for line in text.splitlines() if "uses:" in line]
                self.assertGreater(len(uses_lines), 0)
                for line in uses_lines:
                    match = re.search(
                        r"uses:\s+(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@"
                        r"(?P<sha>[0-9a-f]{40})\s+#\s+(?P<version>v\d+\.\d+\.\d+)\s*$",
                        line,
                    )
                    self.assertIsNotNone(match, line)
                    action = match.group("action")
                    self.assertIn(action, ALLOWED_ACTIONS)
                    observed.setdefault(action, set()).add(
                        (match.group("sha"), match.group("version"))
                    )
                self.assertIn("permissions:", text)
                if "actions/checkout@" in text:
                    checkout_index = text.index("actions/checkout@")
                    checkout_window = text[checkout_index : checkout_index + 240]
                    self.assertIn("persist-credentials: false", checkout_window)

        # 每个 action 在所有 workflow 里必须钉同一个 (sha, version)。这条替代了原来
        # 硬编码的 SHA 表：硬编码值只有 Dependabot 能触发变更、而它改不了测试，于是
        # 每次升级都必然红（PR #18 即为此卡住）。跨文件一致性保留了真正的价值——
        # 抓「只升了一部分 workflow」的半吊子升级——同时不再自锁。
        for action, pins in sorted(observed.items()):
            with self.subTest(action=action):
                self.assertEqual(
                    len(pins),
                    1,
                    f"{action} is pinned inconsistently across workflows: {sorted(pins)}",
                )

    def test_builds_require_verified_pdf_html_and_source_integrity(self) -> None:
        for workflow in BUILD_WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("EXPECTED_README_SHA", text)
                self.assertIn("sha256sum README.md", text)
                self.assertIn("tools/verify_artifacts.py", text)
                self.assertIn("--expected-readme-sha", text)
                self.assertRegex(text, r"mdpress build --format pdf --output dist/[^\s]+\.pdf")
                self.assertIn("tools/build_html_reader.py", text)
                self.assertIn("timeout --signal=TERM 8m python3 tools/render_mermaid.py", text)
                # Mermaid 渲染失败必须让流水线红，不能降级发布带原始源码的版本
                self.assertNotIn("using source fallback", text)
                self.assertIn("Mermaid rendering failed", text)
                self.assertIn("exit 1", text)
                self.assertIn("--pdf", text)
                self.assertIn("--html", text)
                self.assertIn("SHA256SUMS", text)
                self.assertIn("python3 -m unittest discover -s tests -v", text)

        preview = (ROOT / ".github/workflows/preview-pdf.yml").read_text(encoding="utf-8")
        self.assertIn("EXPECTED_README_SHA", preview)
        self.assertIn("sha256sum README.md", preview)
        self.assertIn("python3 tools/verify_artifacts.py", preview)
        self.assertIn("--expected-readme-sha", preview)
        self.assertIn("--pdf dist/ai_beginner_guide.pdf", preview)
        self.assertIn("sha256sum ai_beginner_guide.pdf > SHA256SUMS", preview)
        self.assertIn("sha256sum -c SHA256SUMS", preview)
        self.assertIn("dist/SHA256SUMS", preview)
        self.assertLess(
            preview.index("python3 tools/verify_artifacts.py"),
            preview.index("gh release upload preview-pdf"),
        )

    def test_release_does_not_treat_html_as_optional(self) -> None:
        auto_release = (ROOT / ".github/workflows/auto-release.yml").read_text(encoding="utf-8")
        preview = (ROOT / ".github/workflows/preview-pdf.yml").read_text(encoding="utf-8")
        self.assertNotIn("continue-on-error: true", auto_release)
        for suffix in (".pdf", ".html", "SHA256SUMS"):
            self.assertIn(suffix, auto_release)

        workflows = (
            (auto_release, "release", "ai_beginner_guide-editions"),
            (preview, "publish", "ai_beginner_guide-preview"),
        )
        for text, publish_job_name, artifact_name in workflows:
            with self.subTest(publish_job=publish_job_name):
                global_permissions = text[: text.index("jobs:")]
                build = job_block(text, "build")
                publish = job_block(text, publish_job_name)

                self.assertNotIn("contents: write", global_permissions)
                self.assertIn("permissions:\n      contents: read", build)
                self.assertNotIn("contents: write", build)
                self.assertIn("actions/upload-artifact@", build)
                self.assertIn(f"name: {artifact_name}", build)

                self.assertIn("needs: build", publish)
                self.assertIn("permissions:\n      contents: write", publish)
                self.assertIn("actions/download-artifact@", publish)
                self.assertIn(f"name: {artifact_name}", publish)
                self.assertIn("sha256sum -c SHA256SUMS", publish)
                for forbidden in (
                    "actions/checkout@",
                    "mdpress",
                    "npm install",
                    "curl ",
                    "sudo ",
                    "python3 ",
                    "tools/",
                ):
                    self.assertNotIn(forbidden, publish)

        preview_build = job_block(preview, "build")
        preview_publish = job_block(preview, "publish")
        self.assertNotIn("GH_TOKEN", preview_build)
        self.assertNotIn("github.token", preview_build)
        self.assertIn("GH_TOKEN", preview_publish)
        self.assertIn("github.token", preview_publish)

    def test_preview_publish_steps_follow_tag_release_asset_order(self) -> None:
        preview = (ROOT / ".github/workflows/preview-pdf.yml").read_text(encoding="utf-8")
        synchronize = preview.index("      - name: Synchronize mutable preview tag\n")
        release = preview.index("      - name: Create or update preview release\n")
        upload = preview.index("      - name: Upload verified preview artifacts\n")

        self.assertLess(synchronize, release)
        self.assertLess(release, upload)

    def run_preview_scripts(
        self,
        scenario,
        *,
        repository=TEST_REPOSITORY,
        sha=TEST_SHA,
    ):
        preview = (ROOT / ".github/workflows/preview-pdf.yml").read_text(encoding="utf-8")
        scripts = workflow_step_scripts_in_document_order(
            preview,
            (
                "Synchronize mutable preview tag",
                "Create or update preview release",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_gh = root / "gh"
            fake_gh.write_text(FAKE_GH, encoding="utf-8")
            fake_gh.chmod(0o755)
            log = root / "commands.jsonl"
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{root}:{env.get('PATH', '')}",
                    "GH_LOG": str(log),
                    "GH_SCENARIO": scenario,
                    "GH_TOKEN": "test-token",
                    "GH_REPO": repository,
                    "GITHUB_REPOSITORY": repository,
                    "GITHUB_SHA": sha,
                }
            )
            result = None
            for script in scripts:
                result = subprocess.run(
                    ["/bin/bash", "-c", script],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    break
            commands = []
            if log.exists():
                commands = [
                    json.loads(line)
                    for line in log.read_text(encoding="utf-8").splitlines()
                ]
            return result, commands

    def test_mutable_preview_updates_existing_tag_and_release(self) -> None:
        result, commands = self.run_preview_scripts("ref_200_release_exists")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND, EDIT_RELEASE_COMMAND],
        )

    def test_mutable_preview_creates_only_on_explicit_not_found(self) -> None:
        result, commands = self.run_preview_scripts("ref_404_release_missing")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, POST_REF_COMMAND, VIEW_RELEASE_COMMAND, CREATE_RELEASE_COMMAND],
        )
        flattened = [argument for command in commands for argument in command]
        self.assertNotIn("--target", flattened)

    def test_preview_rejects_invalid_repository_and_sha_before_calling_gh(self) -> None:
        cases = (
            {"repository": "owner/repo/extra", "sha": TEST_SHA, "message": "Invalid GITHUB_REPOSITORY"},
            {"repository": TEST_REPOSITORY, "sha": "a" * 39, "message": "Invalid GITHUB_SHA"},
        )
        for case in cases:
            with self.subTest(case=case):
                result, commands = self.run_preview_scripts(
                    "ref_200_release_exists",
                    repository=case["repository"],
                    sha=case["sha"],
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [])
                self.assertIn(case["message"], result.stderr)

    def test_preview_tag_lookup_fails_closed_on_non_404_errors(self) -> None:
        for scenario in ("ref_401", "ref_403", "ref_429", "ref_503", "ref_network"):
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [GET_REF_COMMAND])
                expected = "network failure" if scenario.endswith("network") else scenario.removeprefix("ref_")
                self.assertIn(expected, result.stderr)

    def test_preview_release_lookup_fails_closed_except_exact_not_found(self) -> None:
        scenarios = (
            "ref_200_release_401",
            "ref_200_release_403",
            "ref_200_release_404",
            "ref_200_release_429",
            "ref_200_release_503",
            "ref_200_release_network",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(
                    commands,
                    [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND],
                )
                expected = "network failure" if scenario.endswith("network") else scenario.rsplit("release_", 1)[1]
                self.assertIn(expected, result.stderr)

    def test_preview_publish_has_explicit_repo_context_only_in_write_job(self) -> None:
        preview = (ROOT / ".github/workflows/preview-pdf.yml").read_text(encoding="utf-8")
        build = job_block(preview, "build")
        publish = job_block(preview, "publish")

        self.assertNotIn("GH_REPO", build)
        self.assertIn("GH_REPO: ${{ github.repository }}", publish)


class ArtifactVerifierTests(unittest.TestCase):
    def test_released_v130_symptom_is_rejected(self) -> None:
        verifier = load_verifier()
        released_text = (ROOT / "tests/fixtures/v1.3.0-released-pages.txt").read_text(
            encoding="utf-8"
        )
        with self.assertRaises(verifier.ArtifactVerificationError):
            verifier.validate_book_text(released_text, expected_title="零基础学 AI")

    def test_clean_book_text_is_accepted(self) -> None:
        verifier = load_verifier()
        verifier.validate_book_text(
            "零基础学 AI\n第一章 走进人工智能世界\n第二章 AI 核心概念速览",
            expected_title="零基础学 AI",
        )
        with patch.object(
            sys,
            "argv",
            [
                "verify_artifacts.py",
                "--readme",
                "README.md",
                "--expected-readme-sha",
                "0" * 64,
                "--pdf",
                "preview.pdf",
            ],
        ):
            try:
                args = verifier.parse_args()
            except SystemExit as error:
                self.fail(f"PDF-only artifact verification must be supported: {error}")
        self.assertIsNone(args.html)

    def test_readme_hash_detects_source_mutation(self) -> None:
        verifier = load_verifier()
        original = ROOT / "README.md"
        expected = hashlib.sha256(original.read_bytes()).hexdigest()
        verifier.verify_readme(original, expected)

        with tempfile.TemporaryDirectory() as temp_dir:
            changed = Path(temp_dir) / "README.md"
            changed.write_text(original.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_readme(changed, expected)

    def test_html_smoke_check_rejects_polluted_content(self) -> None:
        verifier = load_verifier()
        with tempfile.TemporaryDirectory() as temp_dir:
            html_path = Path(temp_dir) / "book.html"
            html_path.write_text(
                "<html><head><title>零基础学 AI</title></head>"
                "<body><h1>Why Teams Use mdPress</h1></body></html>",
                encoding="utf-8",
            )
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_html(html_path, expected_title="零基础学 AI")


if __name__ == "__main__":
    unittest.main()
