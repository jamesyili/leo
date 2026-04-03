# Primers • Partial Derivative for SVM/Hinge Loss

**Source:** https://aman.ai/primers/backprop/derivative-svm/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

the partial derivative of the multiclass hinge loss function that multiclass svm deploys with respect to the weights w j is text for the correct class i e j y i nabla w y i l i left sum j neq y i mathbb 1 w j tx i w y i tx i delta gt 0 right x i text for the incorrect classes i e j neq y i nabla w j l i mathbb 1 w j tx i w y i tx i delta gt 0 x i starting with the svm loss function for a single datapoint l i sum j neq y i left max 0 w j tx i w y i tx i delta right differentiating the function to obtain the gradient with respect to the weights corresponding to the correct class w y i we obtain boxed nabla w y i l i left sum j neq y i mathbb 1 w j tx i w y i tx i delta gt 0 right x i where mathbb 1 cdot is the indicator function that is 1 if the condition inside is true or 0 otherwise note that this is the gradient only with respect to the row of w that corresponds to the correct class to build some intuition as far as this expression goes you re simply counting the number of classes that didn t meet the desired margin and hence contributed to the loss function and then the data vector x i scaled by this count is the effective gradient for the other rows where j neq y i the gradient is boxed nabla w j l i mathbb 1 w j tx i w y i tx i delta gt 0 x i references stanford cs231n optimization notes
