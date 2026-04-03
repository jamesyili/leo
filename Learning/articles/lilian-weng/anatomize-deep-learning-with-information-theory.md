# Anatomize Deep Learning with Information Theory

**Source:** https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

Professor Naftali Tishby passed away in 2021. Hope the post can introduce his cool idea of information bottleneck to more people.

Recently I watched the talk [“Information Theory in Deep Learning”](https://youtu.be/bLqJHjXihK8) by Prof Naftali Tishby and found it very interesting. He presented how to apply the information theory to study the growth and transformation of deep neural networks during training. Using the [Information Bottleneck (IB)](https://arxiv.org/pdf/physics/0004057.pdf) method, he proposed a new learning bound for deep neural networks (DNN), as the traditional learning theory fails due to the exponentially large number of parameters. Another keen observation is that DNN training involves two distinct phases: First, the network is trained to fully represent the input data and minimize the generalization error; then, it learns to forget the irrelevant details by compressing the representation of the input.
