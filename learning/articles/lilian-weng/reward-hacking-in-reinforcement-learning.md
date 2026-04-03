# Reward Hacking in Reinforcement Learning

**Source:** https://lilianweng.github.io/posts/2024-11-28-reward-hacking/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

Reward hacking occurs when a [reinforcement learning (RL)]((https://lilianweng.github.io/posts/2018-02-19-rl-overview/)) agent [exploits](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#exploitation-vs-exploration) flaws or ambiguities in the reward function to achieve high rewards, without genuinely learning or completing the intended task. Reward hacking exists because RL environments are often imperfect, and it is fundamentally challenging to accurately specify a reward function.

With the rise of [language models](https://lilianweng.github.io/posts/2019-01-31-lm/) generalizing to a broad spectrum of tasks and RLHF becomes a de facto method for alignment training, reward hacking in RL training of language models has become a critical practical challenge. Instances where the model learns to modify unit tests to pass coding tasks, or where responses contain biases that mimic a user’s preference, are pretty concerning and are likely one of the major blockers for real-world deployment of more autonomous use cases of AI models.
