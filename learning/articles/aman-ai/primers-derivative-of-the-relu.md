# Primers • Derivative of the ReLU

**Source:** https://aman.ai/primers/backprop/derivative-relu/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

prove that the derivative of the rectified linear unit relu with respect to the input z is frac drelu z dx left begin array ll 0 amp text if z lt 0 1 amp text if z gt 0 end array right recall that the relu performs zero thresholding of the input i e the input cannot be lower than 0 in other words it acts as a gate keeper or a switch and only propagates forward non negative inputs while zeroing out other inputs relu z left begin array ll 0 amp text if z lt 0 z amp text if z gt 0 end array right put simply relu z max 0 z so the output of a relu is either z or 0 depending on whether the input is non negative or negative respectively note that the relu is not defined at 0 so there must be a convention to set it either at 0 or 1 in this case as such the derivative of relu with respect to the input z is boxed frac drelu z dz left begin array ll 0 amp text if z lt 0 1 amp text if z gt 0 end array right intuitively the derivative of the relu indicates that the error either fully propagates to the previous layer owing to the 1 in case if the input to the relu is non negative or is completely stopped owing to the 0 if the input to relu is negative
