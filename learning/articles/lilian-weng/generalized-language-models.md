# Generalized Language Models

**Source:** https://lilianweng.github.io/posts/2019-01-31-lm/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2019-02-14: add [ULMFiT](#ulmfit) and [GPT-2](#gpt-2).]

[Updated on 2020-02-29: add [ALBERT](#albert).]

[Updated on 2020-10-25: add [RoBERTa](#roberta).]

[Updated on 2020-12-13: add [T5](#t5).]

[Updated on 2020-12-30: add [GPT-3](#gpt-3).]

[Updated on 2021-11-13: add [XLNet](#xlnet), [BART](#bart) and [ELECTRA](#electra); Also updated the [Summary](#summary) section.]

	![](elmo-and-bert.png)
	I guess they are Elmo & Bert? (Image source: [here](https://www.youtube.com/watch?v=l5einDQ-Ttc))

We have seen amazing progress in NLP in 2018. Large-scale pre-trained language modes like [OpenAI GPT](https://blog.openai.com/language-unsupervised/) and [BERT](https://arxiv.org/abs/1810.04805) have achieved great performance on a variety of language tasks using generic model architectures. The idea is similar to how ImageNet classification pre-training helps many vision tasks (*). Even better than vision classification pre-training, this simple and powerful approach in NLP does not require labeled data for pre-training, allowing us to experiment with increased training scale, up to our very limit.
