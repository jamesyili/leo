# Generalized Visual Language Models

**Source:** https://lilianweng.github.io/posts/2022-06-09-vlm/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

Processing images to generate text, such as image captioning and visual question-answering, has been studied for years. Traditionally such systems rely on an object detection network as a vision encoder to capture visual features and then produce text via a text decoder. Given a large amount of existing literature, in this post, I would like to only focus on one approach for solving vision language tasks, which is to *extend pre-trained [generalized language models](https://lilianweng.github.io/posts/2019-01-31-lm/) to be capable of consuming visual signals*.
