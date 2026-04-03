# Object Detection for Dummies Part 3: R-CNN Family

**Source:** https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2018-12-20: Remove YOLO here. Part 4 will cover multiple fast object detection algorithms, including YOLO.]

[Updated on 2018-12-27: Add [bbox regression](#bounding-box-regression) and [tricks](#common-tricks) sections for R-CNN.]

In the series of “Object Detection for Dummies”, we started with basic concepts in image processing, such as gradient vectors and HOG, in [Part 1](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/). Then we introduced classic convolutional neural network architecture designs for classification and pioneer models for object recognition, Overfeat and DPM, in [Part 2](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/). In the third post of this series, we are about to review a set of models in the R-CNN (“Region-based CNN”) family.
