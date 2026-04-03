# Large Transformer Model Inference Optimization

**Source:** https://lilianweng.github.io/posts/2023-01-10-inference-optimization/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2023-01-24: add a small section on [Distillation](#distillation).]

Large transformer models are mainstream nowadays, creating SoTA results for a variety of tasks. They are powerful but very expensive to train and use. The extremely high inference cost, in both time and memory, is a big bottleneck for adopting a powerful transformer for solving real-world tasks at scale.

**Why is it hard to run inference for large transformer models?** Besides the increasing size of SoTA models, there are two main factors contributing to the inference challenge ([Pope et al. 2022](https://arxiv.org/abs/2211.05102)):
