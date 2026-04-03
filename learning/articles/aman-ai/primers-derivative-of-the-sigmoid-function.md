# Primers • Derivative of the Sigmoid Function

**Source:** https://aman.ai/primers/backprop/derivative-sigmoid/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

prove that the derivative of the sigmoid function with respect to the input z is frac d d z sigma z sigma z 1 sigma z recall that the sigmoid function is given by sigma z frac 1 1 e z here s how we obtain its derivative begin aligned frac d d z sigma z amp frac d d z left frac 1 1 e z right amp frac d d z left 1 mathrm e z right 1 amp left 1 e z right 2 left e z right amp frac e z left 1 e z right 2 amp frac 1 1 e z cdot frac e z 1 e z amp frac 1 1 e z cdot frac left 1 e z right 1 1 e z amp frac 1 1 e z cdot left frac 1 e z 1 e z frac 1 1 e z right amp frac 1 1 e z cdot left 1 frac 1 1 e z right amp boxed sigma z cdot 1 sigma z end aligned
