# 8 plots that explain the state of open models

**Source:** https://www.interconnects.ai/p/8-plots-that-explain-the-state-of
**Ingested:** 2026-04-02
**Tags:** rlhf, reinforcement-learning, llms

---

Starting 2026, most people are aware that a handful of Chinese companies are making strong, open AI models that are applying increasing pressure on the American AI economy. 

While [many Chinese labs are making models](https://www.interconnects.ai/i/181259397/mapping-the-open-ecosystem), the adoption metrics are dominated by Qwen (with a little help from DeepSeek). Adoption of the new entrants in the open model scene in 2025, from Z.ai, MiniMax, Kimi Moonshot, and others is actually quite limited. This sets up the position where dethroning Qwen in adoption in 2026 looks impossible overall, but there are areas for opportunity. In fact, the strength of GPT-OSS shows that the U.S. could very well have the smartest open models again in 2026, even if they’re used far less across the ecosystem.

The following plots are from a comprehensive update of the data supporting The ATOM Project ([atomproject.ai](https://www.atomproject.ai/)) with our expanded ecosystem measurement tools we use to support our monthly open model roundups, [Artifacts Log](https://www.interconnects.ai/t/artifacts-log).

Interconnects is a reader-supported publication. Consider becoming a subscriber.

1. China has a growing lead in every adoption metric

Models from the US and the EU defined the early eras of open language models. 2025 saw the end of Llama and Qwen triumphantly took its spot as the default models of choice across a variety of tasks, from local LLMs to reasoning models or multimodal tools. The adoption of Chinese models continues to accelerate.

![](https://substackcdn.com/image/fetch/$s_!fz6U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18bc5002-7e0d-4392-b864-83ca777fab58_1818x1498.png)

These first two plots show the cumulative downloads of all LLMs we consider representative of the ecosystem (we’re [tracking 1152 in total right now](https://github.com/Interconnects-AI/tracked-models)), which were released after ChatGPT.

2. The West isn’t close to replacing Llama

Where we’ve seen China’s lead increase in overall downloads in the previous figure, it feels increasingly precarious for supporters of Western open models to learn that Llama models — despite not being updated nor supported by their creator Meta — are still by far the most downloaded Western models in recent months. OpenAI’s GPT-OSS models are the only models from a new provider in the second half of 2025 that show early signs of shifting the needle on the balance of overall downloads from either an American or Chinese provider (OpenAI’s two models get about the same monthly downloads at the end of 2025 as all of DeepSeek’s or Mistral’s models).

![](https://substackcdn.com/image/fetch/$s_!78VP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cd4601b-8db1-4ab7-9fbc-4052987ebd9c_1818x1498.png)

What is a HuggingFace download? HuggingFace registers a download for any web request to the storage buckets to the model (e.g. wget, curl, etc.), so it is a very noisy metric. Still, it’s the best we have. Due to this noise, when measuring adoption via how many finetunes a model has, we filter to derivative models with only >5 downloads. Still, downloads are the standard way of measuring adoption of open models.

3. New organizations barely show up in adoption metrics

While much has been said (including by me, on Interconnects) about new open frontier model providers, their adoption tends to look like a rounding error in adoption metrics. These models from Z.ai, Nvidia, Kimi Moonshot, and MiniMax are crucial to developing local ecosystems, but they are not competing with Qwen as being the open model standard.

Note the different y-axes from this plot and the previous, where DeepSeek and OpenAI are included in both for scale. This plot shows the downloads just since July 2025 to showcase recent performance.

![](https://substackcdn.com/image/fetch/$s_!rcd5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c60de2-eb3d-444a-b3a6-b66f9e202346_1866x1160.png)

4. Qwen’s weakness is in large model adoption

One of the most surprising things in the data is just how successful DeepSeek’s large models are (particularly both versions of V3 and R1). These 4 large models dominate the adoption numbers of any of Qwen’s large MoE/dense models over the last few years. It’s only at these large scales where opportunities to compete with Qwen exist, and with the rise of more providers like Z.ai, MiniMax, and Kimi, we’ll be following this closely. These large models are crucial tools right now for many startups based in the U.S. trying to finetune their own frontier model for applications — e.g. Cursor’s [Composer](https://cursor.com/blog/composer) model is finetuned from a large Chinese MoE.

![](https://substackcdn.com/image/fetch/$s_!L-lz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26a16175-d9e6-4ca9-ae31-46c84f25d693_1872x1156.png)

[Share](https://www.interconnects.ai/p/8-plots-that-explain-the-state-of?utm_source=substack&utm_medium=email&utm_content=share&action=share)

5. A few models from Qwen dwarf new entrants

While Qwen has one Achilles’ heel right now, its recent models totally dominate any HuggingFace metric. If we look at the top 5 Qwen3 downloaded models just in December (Qwen3-[0.6B, 1.7B, 4B (Original), 8B, & 4B-Instruct-2507]), they have more downloads than all of the models we’re tracking from OpenAI, Mistral AI, Nvidia, Z.ai, Moonshot AI, and MiniMax combined. 

This is the advantage that Qwen has built and will take year(s) to unwind.

![](https://substackcdn.com/image/fetch/$s_!IL9W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8e7e64c-0ed6-4b54-b738-afd32c774cae_1864x1160.png)

6. In December Qwen got more downloads than roughly the rest of the open ecosystem

If we account for every meaningful Qwen LLM released since ChatGPT, the downloads Qwen got in December well outnumber literally every other organization we’re tracking combined. This includes the 6 from the previous figure, along with DeepSeek and Meta, who are the second and third most downloaded creators.

![](https://substackcdn.com/image/fetch/$s_!he5w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76454a8e-cd85-4911-b730-9fa8f516ca63_1870x1232.png)

7. People are still finetuning Qwen more than anything else

The other primary way we can measure Qwen’s adoption lead is to look at the share of derivative models on HuggingFace (filtered to only those with >5 downloads to indicate a meaningful finetune) that come from a certain base model. Qwen’s share here continued to grow throughout 2025, and we’ll be watching this closely around the likely release of Qwen 4.

Despite the dramatic increase in the number of players releasing open models in 2025, the share of finetuned models has concentrated among the 5 organizations we highlighted below (Qwen, Llama, Mistral, Google, and DeepSeek).

![](https://substackcdn.com/image/fetch/$s_!-ujU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86726b22-86da-44e3-9566-a9cd4e910d3d_1810x1212.png)

8. China still has the smartest open models

The primary factor that drives the adoption and influence of Chinese open models today is that they’re the smartest open models available. There’s a variety of second order issues, such as licenses, model sizes, documentation, developer engagement, etc., but for over a year now, Chinese open models have been the smartest on most benchmarks.

GPT-OSS 120B was close to retaking the lead (slightly behind MiniMax M2), but it wasn’t quite there. It’ll be fascinating to watch if upcoming Nemotron, Arcee, or Reflection AI models can buck this trend. If you look at other metrics than the Artificial Analysis intelligence index, the same trends hold.

![](https://substackcdn.com/image/fetch/$s_!yl07!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a1d0516-92d4-4f5f-9bd9-2883ff5d7ab5_1964x1750.png)

[Leave a comment](https://www.interconnects.ai/p/8-plots-that-explain-the-state-of/comments)

Thanks for reading! Please reach out or leave a comment if there’s a corner of the data you think we should spend more time in. Stay tuned for more updates on [The ATOM Project](https://www.atomproject.ai/) and related efforts in the near future.
