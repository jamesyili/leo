# Diffusion Models for Video Generation

**Source:** https://lilianweng.github.io/posts/2024-04-12-diffusion-video/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Diffusion models](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) have demonstrated strong results on image synthesis in past years. Now the research community has started working on a harder task—using it for video generation. The task itself is a superset of the image case, since an image is a video of 1 frame, and it is much more challenging because:

It has extra requirements on temporal consistency across frames in time, which naturally demands more world knowledge to be encoded into the model.

In comparison to text or images, it is more difficult to collect large amounts of high-quality, high-dimensional video data, let along text-video pairs.

🥑 Required Pre-read: Please make sure you have read the previous blog on [“What are Diffusion Models?”](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) for image generation before continue here.
