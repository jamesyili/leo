# Thinking about High-Quality Human Data

**Source:** https://lilianweng.github.io/posts/2024-02-05-human-data-quality/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Special thank you to [Ian Kivlichan](https://scholar.google.com/citations?user=FRBObOwAAAAJ&hl=en) for many useful pointers (E.g. the 100+ year old Nature paper “Vox populi”) and nice feedback. 🙏 ]

High-quality data is the fuel for modern data deep learning model training. Most of the task-specific labeled data comes from human annotation, such as classification task or [RLHF](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#rl-fine-tuning-with-human-preferences) labeling (which can be constructed as classification format) for LLM alignment training. Lots of ML techniques in the post can help with data quality, but fundamentally human data collection involves attention to details and careful execution. The community knows the value of high quality data, but somehow we have this subtle impression that “Everyone wants to do the model work, not the data work” ([Sambasivan et al. 2021](https://dl.acm.org/doi/abs/10.1145/3411764.3445518)).
