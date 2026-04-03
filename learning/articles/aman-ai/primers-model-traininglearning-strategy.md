# Primers • Model Training/Learning Strategy

**Source:** https://aman.ai/primers/ai/learning-strategy/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

learning strategy sanity check model architecture citation learning strategysanity check model architecture overfit on a minibatch or a small dataset to ensure that there are no bugs and near perfect performance on the training set is achieved then set the batch size to what fits in the gpu memory for maximum vectorization parallelization overfitting a model on a small mini batch of data is sometimes a useful technique for debugging a deep learning model overfitting on a mini batch means training the model to fit the mini batch perfectly even if it results in poor generalization performance the reason why this can be useful for debugging is that it allows you to quickly identify issues with the model architecture or training process such as high bias or high variance for example if the model is not able to overfit a small mini batch it may indicate that the model is too shallow or has not been trained for enough epochs on the other hand if the model overfits the mini batch too quickly it may indicate that the model is too complex or that the learning rate is too high citationif you found our work useful please cite it as article chadha2020distilledactfunctions title model training learning strategy author chadha aman and jain vinija journal distilled ai year 2020 note url https aman ai
