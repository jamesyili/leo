# Primers • Derivative of the tanh function

**Source:** https://aman.ai/primers/backprop/derivative-tanh/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

prove that the derivative of the tanh function with respect to the input z is frac d tanh z d z 1 tanh 2 z frac 1 cosh 2 z recall that the tanh function is given by tanh z frac e z e z e z e z per the quotient rule of derivatives frac d f g d z frac g f prime f g prime g 2 set f sinh z g cosh z to get frac d tanh z d z frac cosh z cdot sinh z prime sinh z cdot cosh z prime cosh 2 z now begin array l sinh z prime frac 1 2 left e z e z right cosh z cosh z prime frac 1 2 left e z e z right sinh z end array thus frac d tanh z d z frac cosh 2 z sinh z 2 cosh 2 z 1 left frac sinh z cosh z right 2 1 tanh 2 z now frac 1 cosh 2 z 1 tanh 2 z proof 1 frac sinh 2 z cosh 2 z frac cosh 2 z sinh 2 z cosh 2 z operatorname since left cosh 2 z right left sinh 2 z right 1 frac 1 cosh 2 z operatorname sech 2 z thus boxed frac d tanh z d z 1 tanh 2 z frac 1 cosh 2 z references quotient rule of derivatives
