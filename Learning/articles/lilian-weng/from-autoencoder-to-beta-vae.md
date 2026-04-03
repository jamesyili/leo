# From Autoencoder to Beta-VAE

**Source:** https://lilianweng.github.io/posts/2018-08-12-vae/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2019-07-18: add a section on [VQ-VAE & VQ-VAE-2](#vq-vae-and-vq-vae-2).]

[Updated on 2019-07-26: add a section on [TD-VAE](#td-vae).]

Autocoder is invented to reconstruct high-dimensional data using a neural network model with a narrow bottleneck layer in the middle (oops, this is probably not true for [Variational Autoencoder](#vae-variational-autoencoder), and we will investigate it in details in later sections). A nice byproduct is dimension reduction: the bottleneck layer captures a compressed latent encoding. Such a low-dimensional representation can be used as en embedding vector in various applications (i.e. search), help data compression, or reveal the underlying data generative factors.
