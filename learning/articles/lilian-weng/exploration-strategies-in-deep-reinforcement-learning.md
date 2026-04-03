# Exploration Strategies in Deep Reinforcement Learning

**Source:** https://lilianweng.github.io/posts/2020-06-07-exploration-drl/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

[Updated on 2020-06-17: Add [“exploration via disagreement”](#exploration-via-disagreement) in the “Forward Dynamics” [section](#forward-dynamics).

[Exploitation versus exploration](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/) is a critical topic in Reinforcement Learning. We’d like the RL agent to find the best solution as fast as possible. However, in the meantime, committing to solutions too quickly without enough exploration sounds pretty bad, as it could lead to local minima or total failure. Modern [RL](https://lilianweng.github.io/posts/2018-02-19-rl-overview/) [algorithms](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) that optimize for the best returns can achieve good exploitation quite efficiently, while exploration remains more like an open topic.
