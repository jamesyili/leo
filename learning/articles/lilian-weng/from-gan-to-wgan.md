# From GAN to WGAN

**Source:** https://lilianweng.github.io/posts/2017-08-20-gan/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2018-09-30: thanks to Yoonju, we have this post translated in [Korean](https://github.com/yjucho1/articles/blob/master/fromGANtoWGAN/readme.md)!]

[Updated on 2019-04-18: this post is also available on [arXiv](https://arxiv.org/abs/1904.08994).]

[Generative adversarial network](https://arxiv.org/pdf/1406.2661.pdf) (GAN) has shown great results in many generative tasks to replicate the real-world rich content such as images, human language, and music. It is inspired by game theory: two models, a generator and a critic, are competing with each other while making each other stronger at the same time. However, it is rather challenging to train a GAN model, as people are facing issues like training instability or failure to converge.
