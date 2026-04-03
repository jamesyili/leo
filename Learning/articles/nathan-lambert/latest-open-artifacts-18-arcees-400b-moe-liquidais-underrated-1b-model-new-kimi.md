# Latest open artifacts (#18): Arcee's 400B MoE, LiquidAI's underrated 1B model, new Kimi, and anticipation of a busy month

**Source:** https://www.interconnects.ai/p/latest-open-artifacts-18-arcees-big
**Ingested:** 2026-04-02
**Tags:** rlhf, reinforcement-learning, llms

---

January was on the slower side of open model releases compared to the record-setting year that was 2025. While there were still plenty of very strong and noteworthy models, most of the AI industry is looking ahead to models coming soon. There have [been](https://www.bloomberg.com/news/articles/2026-01-27/china-s-moonshot-unveils-new-ai-model-ahead-of-deepseek-release?utm_source=chatgpt.com) [countless](https://www.theinformation.com/articles/deepseek-release-next-flagship-ai-model-strong-coding-ability?utm_source=chatgpt.com) [rumors](https://www.reuters.com/technology/deepseek-launch-new-ai-model-focused-coding-february-information-reports-2026-01-09/?utm_source=chatgpt.com) of DeepSeek V4’s looming release and impressive capabilities alongside a far more competitive open model ecosystem.

In the general AI world, [rumors](https://www.reddit.com/r/singularity/comments/1qtc4jg/sonnet_5_next_week/) for Claude Sonnet 5’s release potentially being *tomorrow* have been under debate all weekend. We’re excited for what comes next — for now, plenty of new open models to tinker with.

[Share](https://www.interconnects.ai/p/latest-open-artifacts-18-arcees-big?utm_source=substack&utm_medium=email&utm_content=share&action=share)

**Our Picks**

**[LFM2.5-1.2B-Instruct](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct)** by [LiquidAI](https://huggingface.co/LiquidAI): Liquid continued pretraining from 10T (of their 2.0 series) to 28T tokens and it shows! This model update really surprised us: In our vibe testing, it came very close to Qwen3 4B 2507 Instruct, which we use every day. And this model is over 3 times smaller! In a direct comparison against the (still bigger) Qwen3 1.6B, we preferred LFM2.5 basically every time. And this time, they released all the other variants at once, i.e., a [Japanese](https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP) version, a [vision](https://huggingface.co/LiquidAI/LFM2.5-VL-1.6B) and an [audio model](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B).

![image](https://substackcdn.com/image/fetch/$s_!jthG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff45dd0ef-1d07-4c9e-9150-55d0524114f1_1896x1334.png)

**[Trinity-Large-Preview](https://huggingface.co/arcee-ai/Trinity-Large-Preview)** by [arcee-ai](https://huggingface.co/arcee-ai): An ultra-sparse MoE with 400B total and 13B active parameters, trained by an American company. They also released [a tech report](https://github.com/arcee-ai/trinity-large-tech-report/blob/main/Arcee%20Trinity%20Large.pdf) and two base models, one “true” [base](https://huggingface.co/arcee-ai/Trinity-Large-TrueBase) model pre-annealing and the [base model](https://huggingface.co/arcee-ai/Trinity-Large-Base) after the pre-training phase. Many more insights, including technical details and their motivation, can be found in our interview with the founders and pre-training lead:

**[Kimi-K2.5](https://huggingface.co/moonshotai/Kimi-K2.5)** by [moonshotai](https://huggingface.co/moonshotai): A continual pre-train on 15T tokens. Furthermore, this model is also multimodal! People on Twitter have [replaced Claude 4.5 Opus with K2.5](https://x.com/thdxr/status/2017756481559339221?s=20) for tasks that need a less capable but cheaper model. However, the writing capabilities that K2 and its successor were known for have suffered in favor of coding and agentic abilities.

**[GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash)** by [zai-org](https://huggingface.co/zai-org): A smaller version of GLM-4.7 which comes in the same size as the small Qwen3 MoE with 30B total, 3B active parameters.

**[K2-Think-V2](https://huggingface.co/LLM360/K2-Think-V2)** by [LLM360](https://huggingface.co/LLM360): A truly open reasoning model building on top of their previous line of models.

**Models**

Reading through the rest of this issue, we were impressed by the quality of the “niche” small models across the ecosystem. From OCR to embeddings and song-generation, this issue has some of everything and there really tends to be open models that excel at any modality needed today — they can just be hard to find!

      

          
              Read more
