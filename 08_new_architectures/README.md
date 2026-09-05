# 第八章 新架构与创新案例

> 从 Transformer 的天花板到 SSM 混合架构，再到 DeepSeek 的低成本奇迹

---

Transformer 架构统治了 AI 世界近十年，但它并非完美——二次复杂度（O(N²)）让处理超长文本变得极其昂贵。2024 年起，状态空间模型（SSM）和混合架构（Mamba、Jamba）开始挑战这一格局。

与此同时，DeepSeek 披露其一次代表性训练运行的成本约 560 万美元（注意这是单次运行，不等于全部研发投入），证明了架构创新和工程效率可以击败规模堆叠。

本章将这两条技术线索合为一体：先理解“为什么需要新架构”，再看“新架构如何在实践中大放异彩”。

## 本章内容

**Part A：超越 Transformer**

- **[8.1 Transformer 的二次复杂度](8.1_transformer_limitation.md)**：理解注意力机制的根本瓶颈
- **[8.2 状态空间模型入门](8.2_ssm_basics.md)**：用初学者友好的比喻理解 SSM
- **[8.3 混合架构的未来](8.3_hybrid_architectures.md)**：Jamba、Bamba、Titans 如何结合两者优势
- **[8.4 长上下文与持久记忆](8.4_long_context.md)**：新架构对 AI 应用的深远影响

**Part B：DeepSeek 深度解析**

- **[8.5 DeepSeek 的故事](8.5_deepseek_story.md)**：从小公司到 AI 独角兽
- **[8.6 MLA 架构与 MoE 创新](8.6_mla_moe_innovation.md)**：多头潜在注意力与混合专家如何优化效率
- **[8.7 DeepSeek-R1 推理模型](8.7_deepseek_r1.md)**：为什么 DeepSeek 能在推理上与 o1 竞争
