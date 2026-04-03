# Domain Randomization for Sim2Real Transfer

**Source:** https://lilianweng.github.io/posts/2019-05-05-domain-randomization/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, deep-learning

---

In Robotics, one of the hardest problems is how to make your model transfer to the real world. Due to the sample inefficiency of deep RL algorithms and the cost of data collection on real robots, we often need to train models in a simulator which theoretically provides an infinite amount of data. However, the reality gap between the simulator and the physical world often leads to failure when working with physical robots. The gap is triggered by an inconsistency between physical parameters (i.e. friction, kp, damping, mass, density) and, more fatally, the incorrect physical modeling (i.e. collision between soft surfaces).
