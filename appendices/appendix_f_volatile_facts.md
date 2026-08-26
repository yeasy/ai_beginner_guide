# 附录 F：快变事实核验表

> `verified_at`: 2026-08-25 · `expires_at`: 2026-09-24 · `ttl_days`: 30

本表是模型名称、可用性、价格、上下文窗口和产品状态的唯一维护入口。超过 `expires_at` 后，项目检查会失败；更新日期前必须重新打开对应官方来源。正文只保留教学所需的短快照，并链接回本表，避免复制容易冲突的状态说明。

| 类别 | 已核验口径 | 官方来源 | 正文写法 |
| --- | --- | --- | --- |
| OpenAI | 模型、API、价格与弃用状态均以当前官方目录为准，不把单一型号写成永久最佳。 | [Models](https://developers.openai.com/api/docs/models/all/), [Pricing](https://openai.com/api/pricing/) | 说明任务、成本和能力取舍；具体版本回链本表。 |
| Anthropic | **Fable 5 已于 2026-07-01 恢复全球访问**；**Mythos 5 仍为受限可用**。**Claude Sonnet 5** 已面向各方案和 Claude Platform 发布，API ID 为 `claude-sonnet-5`。当前官方比较表列出 Fable 5、Opus 5、Sonnet 5 与 Haiku 4.5；**Mythos 5 不在这张比较表里**，它有独立模型页，状态为 Active（invite only），**Opus 4.8 等 4.x 型号已移入 legacy（旧版）区**，仍可用但官方建议迁移；其中 Fable 5 的 Adaptive Thinking 常开，Opus 5 与 Sonnet 5 支持 Adaptive Thinking，Haiku 4.5 支持 Extended Thinking。不确定选哪个时，官方建议从 Opus 5 开始。 | [Fable 5 恢复公告](https://www.anthropic.com/news/redeploying-fable-5), [Sonnet 5 发布公告](https://www.anthropic.com/news/claude-sonnet-5), [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | 区分广泛可用与受限可用；性能和价格按任务核验，不沿用旧状态。 |
| Google Gemini | 型号、预览/稳定状态和迁移窗口以 Gemini API 当前模型页与弃用页为准。 | [Models](https://ai.google.dev/gemini-api/docs/models), [Deprecations](https://ai.google.dev/gemini-api/docs/deprecations) | 明确稳定、预览或迁移状态，不使用非官方型号名。 |
| 开放权重模型 | Llama、DeepSeek、Qwen、Mistral 等以项目发布页、技术报告和 model card 为准。 | 各项目官方 GitHub、model card 与发布博客 | 本地部署成本写成条件判断，不写“免费无限制”。 |
| 量子与硬件 | 路线图和硬件规格以厂商或研究机构的一手资料为准。 | IBM Quantum、NVIDIA、Google、NIST 等官方资料 | 避免把研究目标写成现成能力。 |

维护时只更新有官方证据的条目，并同步受影响正文；若来源之间冲突，保留更保守的可用性表述并记录来源差异。
