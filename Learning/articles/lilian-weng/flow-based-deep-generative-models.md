# Flow-based Deep Generative Models

**Source:** https://lilianweng.github.io/posts/2018-10-13-flow-models/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

So far, I’ve written about two types of generative models, [GAN](https://lilianweng.github.io/posts/2017-08-20-gan/) and [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/). Neither of them explicitly learns the probability density function of real data, $p(\mathbf{x})$ (where $\mathbf{x} \in \mathcal{D}$) — because it is really hard! Taking the generative model with latent variables as an example, $p(\mathbf{x}) = \int p(\mathbf{x}\vert\mathbf{z})p(\mathbf{z})d\mathbf{z}$ can hardly be calculated as it is intractable to go through all possible values of the latent code $\mathbf{z}$.
