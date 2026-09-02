from __future__ import annotations

import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

import check_project_rules as rules


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "appendices/appendix_f_volatile_facts.md"
AFFECTED_CHAPTERS = (
    ROOT / "06_llm/6.5_major_llms.md",
    ROOT / "07_reasoning_models/7.4_major_reasoning_models.md",
    ROOT / "07_reasoning_models/README.md",
    ROOT / "07_reasoning_models/summary.md",
    ROOT / "10_ai_tools/10.2_claude.md",
)


def run_ttl_check(path: Path, today: date) -> list[str]:
    if not hasattr(rules, "check_volatile_facts"):
        raise AssertionError("check_project_rules.py must define check_volatile_facts()")
    return rules.check_volatile_facts(path=path, today=today)


class VolatileFactTtlTests(unittest.TestCase):
    def _write_ledger(self, directory: str, verified: str, expires: str, ttl: int) -> Path:
        path = Path(directory) / "facts.md"
        path.write_text(
            "# Facts\n\n"
            f"> `verified_at`: {verified} · `expires_at`: {expires} · `ttl_days`: {ttl}\n",
            encoding="utf-8",
        )
        return path

    def test_fresh_30_day_metadata_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_ledger(directory, "2026-07-09", "2026-08-08", 30)
            self.assertEqual(run_ttl_check(path, date(2026, 7, 20)), [])

    def test_expired_metadata_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_ledger(directory, "2026-07-09", "2026-08-08", 30)
            issues = run_ttl_check(path, date(2026, 8, 9))
            self.assertTrue(any("expired" in issue for issue in issues), issues)

    def test_non_30_day_window_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_ledger(directory, "2026-07-09", "2026-09-07", 60)
            issues = run_ttl_check(path, date(2026, 7, 9))
            self.assertTrue(any("30 days" in issue for issue in issues), issues)

    def test_main_project_check_enforces_ttl(self) -> None:
        source = (ROOT / "check_project_rules.py").read_text(encoding="utf-8")
        self.assertIn("issues.extend(check_volatile_facts())", source)
        # Check the real ledger as of its OWN verified_at rather than a hardcoded
        # date. This line used to pin 2026-07-09, so re-verifying the ledger — the
        # one thing the TTL exists to force — failed here with "verified_at cannot
        # be in the future". The fixtures above keep fixed dates on purpose; they
        # exercise the checker, not the ledger.
        stamped = re.search(
            r"`verified_at`:\s*(\d{4})-(\d{2})-(\d{2})",
            LEDGER.read_text(encoding="utf-8"),
        )
        self.assertIsNotNone(stamped, "ledger header must carry verified_at")
        self.assertEqual(
            run_ttl_check(LEDGER, date(*(int(g) for g in stamped.groups()))), []
        )


class VolatileFactContentTests(unittest.TestCase):
    def test_ledger_records_current_official_claude_status(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        # Assert the SHAPE of the header, not the literal dates. Pinning the dates
        # here means every legitimate re-verification — the one thing the TTL
        # exists to force — also breaks this test. The date arithmetic is already
        # enforced by check_volatile_facts() against the ledger's own verified_at.
        self.assertRegex(
            text,
            r"`verified_at`: \d{4}-\d{2}-\d{2} · "
            r"`expires_at`: \d{4}-\d{2}-\d{2} · `ttl_days`: 30",
        )
        for required in (
            "Fable 5 已于 2026-07-01 恢复全球访问",
            "Mythos 5 仍为受限可用",
            "Claude Sonnet 5",
            "`claude-sonnet-5`",
            "Claude Fable 5.1 于 2026-09-01 发布",
            "Fable 5.1、Opus 5、Sonnet 5 与 Haiku 4.5",
            "Fable 5 已与 Opus 4.8 等 4.x 型号一同移入 legacy（旧版）区",
            "https://www.anthropic.com/news/redeploying-fable-5",
            "https://www.anthropic.com/news/claude-sonnet-5",
            "https://www.anthropic.com/claude-fable-and-mythos-5-1",
            "https://platform.claude.com/docs/en/models/overview",
        ):
            self.assertIn(required, text)

    def test_affected_chapters_point_to_ledger_and_include_sonnet_5(self) -> None:
        for chapter in AFFECTED_CHAPTERS:
            with self.subTest(chapter=chapter.relative_to(ROOT)):
                text = chapter.read_text(encoding="utf-8")
                self.assertIn("Claude Sonnet 5", text)
                self.assertIn("appendix_f_volatile_facts.md", text)

    def test_no_stale_pause_status_is_copied_outside_ledger(self) -> None:
        stale_phrases = ("暂停访问", "访问暂停", "暂停 Fable 5", "暂停两者访问")
        for path in ROOT.rglob("*.md"):
            if path == LEDGER or any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for phrase in stale_phrases:
                with self.subTest(path=path.relative_to(ROOT), phrase=phrase):
                    self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
