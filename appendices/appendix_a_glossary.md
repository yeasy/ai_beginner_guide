# 附录 A：AI 核心术语表

## A

**智能体（Agent）**
以大语言模型为大脑，具备感知、规划和行动能力的 AI 系统。详见[第十二章](../12_agents/README.md)。

**人工智能 （AI）**
让机器模拟人类智能的技术，包括学习、推理、感知等能力。

**边缘 AI**
在终端设备本地运行的 AI

**通用人工智能（Artificial General Intelligence/AGI）**
具备与人类同等或超越人类的通用智能，能处理各种任务的 AI。

## C

**思维链（Chain of Thought/CoT）**
一种提示技巧，要求模型展示推理步骤，提高逻辑题准确率。详见[第十章第一节](../10_prompt_advanced/10.1_chain_of_thought.md)。

**ChatGPT**
OpenAI 开发的聊天机器人，基于 GPT 模型。详见[第八章第一节](../08_ai_tools/8.1_chatgpt.md)。

**Claude**
Anthropic 开发的 AI，擅长长文本和写作。详见[第八章第二节](../08_ai_tools/8.2_claude.md)。

**CLIP**
图像和文本对齐的模型

**上下文窗口（Context Window）**
模型一次能“记住”或处理的文本长度。

## D

**Deepfake**
AI 生成的虚假视频

**深度学习 （DL）**
机器学习的一种，使用多层神经网络模拟人脑的学习方式，擅长处理图像、语音等复杂数据。

## F

**微调（Fine-tuning）**
在预训练基础上，用特定数据进一步训练，让模型适应特定任务。

## G

**生成式 AI（Generative AI/GenAI）**
能创造新内容（文本、图像、代码等）的 AI，如 ChatGPT。

**GPU**
图形处理器，深度学习的主要计算硬件

## H

**Hugging Face**
AI 模型和数据集的共享平台

## I

**推理 （Inference）**
让训练好的大模型在云端运行、回答问题的过程

## K

**KV Cache**
大模型的“记事本”，缓存已读内容的中间状态以避免重复计算

## L

**大语言模型（Large Language Model/LLM）**
经过海量文本训练的、参数巨大的深度学习模型，能理解和生成人类语言。详见[第六章](../06_llm/README.md)。

## M

**MaaS**
模型即服务，按需调用云上模型的模式

**Midjourney**
著名的 AI 绘画工具，基于 Discord 使用。详见[第七章第二节](../07_multimodal_genai/7.2_image_generation.md)。

**机器学习 （ML）**
AI 的一个子集，让计算机从数据中学习规律，而不是通过编写明确规则。

## P

**参数（Parameters）**
模型内部的变量，相当于模型的“脑细胞”。参数越多，通常模型越强。

**预训练（Pre-training）**
在海量数据上进行的初步训练，让模型获得通用知识。

**提示词工程（Prompt Engineering）**
设计输入的提示词，以引导模型生成更准确、高质量输出的技术。详见[第九章](../09_prompt_basics/README.md)和[第十章](../10_prompt_advanced/README.md)。

**提示词注入（Prompt Injection）**
通过构造恶意输入让模型偏离系统指令，诱导泄露信息或触发高风险操作。详见[第十三章第二节](../13_ethics_future/13.2_safety.md)。

**PyTorch**
Meta 开发的深度学习框架

## R

**RAG**
检索增强生成，先查资料再回答

**ReAct（推理+行动）**
智能体的经典思考模式，结合推理（Reasoning）和行动（Acting）。详见[第十二章第二节](../12_agents/12.2_planning_action.md)。

**人类反馈强化学习（Reinforcement Learning from Human Feedback/RLHF）**
基于人类反馈的强化学习，用于调整模型，使其回答更符合人类偏好。

**检索增强生成（Retrieval-Augmented Generation/RAG）**
结合外部知识库检索和生成模型，解决模型知识幻觉和时效性问题。详见[第十二章第三节](../12_agents/12.3_no_code_platform.md)。

**RLHF**
人类反馈强化学习，让模型对齐人类偏好

## S

**Stable Diffusion**
开源的 AI 绘画模型。详见[第七章第二节](../07_multimodal_genai/7.2_image_generation.md)。

## T

**温度（Temperature）**
控制模型输出随机性的参数。温度越高，结果越有创意但越不可控；温度越低，结果越确定。

**TensorFlow**
Google 开发的深度学习框架

**词元（Token）**
大语言模型（LLM）处理文本的基本单位。对于英文通常是一个词或词根，中文通常是一个字或词。

**Token**
文本的基本处理单位（由分词器切分）

**TPU**
Google 的张量处理单元，专用 AI 芯片

**Transformer 架构（Transformer Architecture）**
目前的 AI 架构基石，基于注意力机制，特别是自注意力机制。详见[第五章第三节](../05_deep_learning/5.3_architectures.md)。

**TTS**
文本到语音合成

## V

**显存 （VRAM）**
GPU 专用内存，大模型运行时的核心瓶颈资源

## 其他

**卷积**
CNN 中提取局部特征的操作

**图灵测试**
评估机器是否展现智能的思想实验

**多模态**
同时处理多种类型的数据

**学习率**
控制每一步参数更新幅度的超参数

**幻觉**
AI 一本正经地编造虚假内容

**弱人工智能**
只能在特定任务上表现智能的 AI 系统

**强人工智能**
具备人类水平通用智能的 AI（尚未实现）

**强化学习**
通过与环境交互获得反馈来学习

**归纳法**
从具体现象总结一般规律的推理方法

**扩散模型**
通过去噪过程生成图像的方法

**指令微调**
让模型学会遵循指令

**损失函数**
量化预测与真实值差距的函数

**掩码**
自监督学习中遮盖部分数据的方法

**梯度下降**
沿“下坡”方向优化参数的方法

**注意力机制**
Transformer 的核心，能聚焦最相关的信息

**激活函数**
引入非线性的函数（如 ReLU）

**神经网络**
模拟人脑结构的计算模型

**聚类**
将相似样本分到同一组

**训练**
模型从数据中学习的过程

**降维**
减少数据维度同时保留重要信息

**黑盒**
无法解释内部逻辑的模型
