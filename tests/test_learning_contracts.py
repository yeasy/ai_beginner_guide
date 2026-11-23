from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
LEARNING_PATH = (ROOT / "appendices/appendix_d_learning_path.md").read_text(encoding="utf-8")
LABS_README = (ROOT / "labs/README.md").read_text(encoding="utf-8")

A_PREREQUISITES = (
    "无需编程或高等数学基础",
    "可使用浏览器和任一对话式 AI 工具",
    "准备一个不含敏感信息的真实任务",
)
A_DELIVERABLES = (
    "一份三轮提示词迭代记录",
    "一份事实核验清单",
    "一张个人场景工作流卡",
)
A_ACCEPTANCE = (
    "能用自己的话区分 AI、机器学习与深度学习",
    "能比较三轮输出并说明改动理由",
    "能为关键事实给出来源，并标出不确定项",
    "能识别隐私、幻觉与自动化越权风险",
)
B_PREREQUISITES = (
    "达到 A 轨验收标准或具备同等基础",
    "Python 3.11+",
    "会在命令行运行 Python 文件",
    "一台可进行 CPU 计算的电脑",
)
B_DELIVERABLES = (
    "五份实验结果字典与自评记录",
    "一份失败案例与排障记录",
    "一份最小 AI 工作流设计",
)
B_ACCEPTANCE = (
    "能复现实验的固定输入与预期范围",
    "能解释每项评估为何通过或失败",
    "能在不使用在线 API 和密钥的情况下完成五个实验",
    "能把评估结果映射回对应章节的核心概念",
)
LAB_MAPPINGS = (
    "| `01_ml_basics.py` | 第 4 章 | 线性回归指标报告 | `evaluate()` 返回 `passed=True` |",
    "| `02_structured_output.py` | 第 12.2 节 | 三个结构化输出校验结果 | `evaluate()` 返回 `passed=True` |",
    "| `03_dl_overfitting.py` | 第 5 章 | 训练/验证损失与早停点 | `evaluate()` 返回 `passed=True` |",
    "| `04_rag_minimal.py` | 第 12.5 节 | 检索命中、上下文与回答 | `evaluate()` 返回 `passed=True` |",
    "| `05_agent_evals.py` | 第 14 章 | 两个案例的智能体评估报告 | `evaluate()` 返回 `passed=True` |",
)


class LearningContractTests(unittest.TestCase):
    def test_readme_links_to_the_online_learning_contract_and_lab_instructions(self) -> None:
        self.assertIn(
            "](https://yeasy.gitbook.io/ai_beginner_guide/fu-lu/appendix_d_learning_path)",
            README,
        )
        self.assertIn(
            "](https://github.com/yeasy/ai_beginner_guide/blob/main/labs/README.md#运行方式)",
            README,
        )

    def test_a_route_has_exact_entry_output_and_acceptance_contract(self) -> None:
        for phrase in A_PREREQUISITES + A_DELIVERABLES + A_ACCEPTANCE:
            self.assertIn(phrase, LEARNING_PATH)

    def test_b_route_has_exact_entry_output_and_acceptance_contract(self) -> None:
        for document in (LEARNING_PATH, LABS_README):
            for phrase in B_PREREQUISITES + B_DELIVERABLES + B_ACCEPTANCE:
                self.assertIn(phrase, document)

    def test_all_five_labs_have_one_canonical_mapping(self) -> None:
        for mapping in LAB_MAPPINGS:
            self.assertIn(mapping, LEARNING_PATH)
            self.assertIn(mapping, LABS_README)

    def test_lab_contract_is_local_cpu_only_and_key_free(self) -> None:
        for phrase in (
            "固定输入",
            "预期范围",
            "排障",
            "自评量表",
            "仅使用 CPU",
            "无需在线 API 或密钥",
        ):
            self.assertIn(phrase, LABS_README)


if __name__ == "__main__":
    unittest.main()
