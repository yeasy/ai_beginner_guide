# 第七章 推理模型与推理计算

> 从快速反应到深入思考：理解 AI“慢思考”革命与推理计算的崛起

---

2024 年底，一个重大转变正在 AI 领域发生。传统的大语言模型都在追求“快速反应”——输入提示词，瞬间得到答案。但现在，一个新的思路正在成为主流：**给 AI 充足的时间来思考**。

这就是“推理模型”（Reasoning Models）的核心理念。OpenAI 从 o 系列演进到 GPT-5 及其迭代版本；Anthropic 从 Extended Thinking 演进到 Claude Fable 5 与 **Claude Sonnet 5** 等新一代型号所采用的 Adaptive Thinking；DeepSeek-R1 则展示了开放权重推理路线。版本与可用性以[快变事实核验表](../appendices/appendix_f_volatile_facts.md)为准。

## 本章内容

- **7.1 两种思维方式：System 1 vs System 2**：理解为什么有时候快速反应，有时候需要深入思考
- **7.2 推理模型的工作原理**：解析 OpenAI o 系列到 GPT-5 及其迭代版本、Claude Extended Thinking 等模型如何进行“思考”
- **7.3 推理计算（Inference-Time Compute）**：掌握新的计算范式
- **7.4 各主流推理模型对比**：深度求索 R1、OpenAI 推理路线、Claude Extended Thinking 和 Adaptive Thinking 的核心差异
- **7.5 推理模型的局限与成本**：认识到思考的代价

## 为什么这章很重要？

在 2025-2026 年，推理模型正在快速成为主流。如果你想理解当代 AI 的最新技术方向，就必须理解推理计算如何工作。这不仅影响开发者如何构建应用，也影响普通用户如何更有效地使用 AI 工具。
