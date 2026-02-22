# 附录 A：AI 核心术语表

> 遇到看不懂的词？来这里查。

---

## 基础概念

**人工智能（Artificial Intelligence/AI）**
让机器模拟人类智能的技术，包括学习、推理、感知等能力。

**机器学习（Machine Learning/ML）**
AI 的一个子集，让计算机从数据中学习规律，而不是通过编写明确规则。

**深度学习（Deep Learning/DL）**
机器学习的一种，使用多层神经网络模拟人脑的学习方式，擅长处理图像、语音等复杂数据。

**生成式 AI（Generative AI/GenAI）**
能创造新内容（文本、图像、代码等）的 AI，如 ChatGPT。

**通用人工智能（Artificial General Intelligence/AGI）**
具备与人类同等或超越人类的通用智能，能处理各种任务的 AI。

## 模型与技术

**大语言模型（Large Language Model/LLM）**
经过海量文本训练的、参数巨大的深度学习模型，能理解和生成人类语言。详见[第六章](../06_llm/README.md)。

**[Transformer 架构](../06_llm/6.1_evolution.md)**
目前的 AI 架构基石，基于注意力机制，特别是自注意力机制。详见[第六章第一节](../06_llm/6.1_evolution.md)。

**词元（Token）**
大语言模型（LLM）处理文本的基本单位。对于英文通常是一个词或词根，中文通常是一个字或词。

**参数（Parameters）**
模型内部的变量，相当于模型的“脑细胞”。参数越多，通常模型越强。

**上下文窗口（Context Window）**
模型一次能“记住”或处理的文本长度。

## 训练与优化

**预训练（Pre-training）**
在海量数据上进行的初步训练，让模型获得通用知识。

**微调（Fine-tuning）**
在预训练基础上，用特定数据进一步训练，让模型适应特定任务。

**人类反馈强化学习（RLHF / Reinforcement Learning from Human Feedback）**
基于人类反馈的强化学习，用于调整模型，使其回答更符合人类偏好。

**提示词工程（Prompt Engineering）**
设计输入的提示词，以引导模型生成更准确、高质量输出的技术。详见[第九章](../09_prompt_basics/README.md)和[第十章](../10_prompt_advanced/README.md)。

**[思维链（Chain of Thought/CoT）](../10_prompt_advanced/10.1_chain_of_thought.md)**
一种提示技巧，要求模型展示推理步骤，提高逻辑题准确率。详见[第十章第一节](../10_prompt_advanced/10.1_chain_of_thought.md)。

**检索增强生成（Retrieval-Augmented Generation/RAG）**
结合外部知识库检索和生成模型，解决模型知识幻觉和时效性问题。详见[第十二章第三节](../12_agents/12.3_no_code_platform.md)。

**温度（Temperature）**
控制模型输出随机性的参数。温度越高，结果越有创意但越不可控；温度越低，结果越确定。

**提示词注入（Prompt Injection）**
通过构造恶意输入让模型偏离系统指令，诱导泄露信息或触发高风险操作。详见[第十三章第二节](../13_ethics_future/13.2_safety.md)。

## 常见工具

**ChatGPT**
OpenAI 开发的聊天机器人，基于 GPT 模型。详见[第八章第一节](../08_ai_tools/8.1_chatgpt.md)。

**Claude**
Anthropic 开发的 AI，擅长长文本和写作。详见[第八章第二节](../08_ai_tools/8.2_claude.md)。

**Midjourney**
著名的 AI 绘画工具，基于 Discord 使用。详见[第七章](../07_multimodal_genai/7.2_image_generation.md)。

**Stable Diffusion**
开源的 AI 绘画模型。详见[第七章](../07_multimodal_genai/7.2_image_generation.md)。

**[智能体（Agent）](../12_agents/README.md)**
以大语言模型为大脑，具备感知、规划和行动能力的 AI 系统。详见[第十二章](../12_agents/README.md)。

**[ReAct（推理+行动）](../12_agents/12.2_planning_action.md)**
智能体的经典思考模式，结合推理（Reasoning）和行动（Acting）。详见[第十二章第二节](../12_agents/12.2_planning_action.md)。
