# Models • Alpaca

**Source:** https://aman.ai/primers/ai/alpaca/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals

---

overview referencesoverview stanford s alpaca is an instruction finetuned 7b language transformer based on the 7b llama gpt 3 alternative by meta released in mid march 2023 instead of using reinforcement learning with human feedback rlhf they take a supervised approach using 52k instruction output pairs instead of using human generated instruction output pairs they retrieve the data by querying the gpt 3 based text davinci 003 model so alpaca essentially uses a form of weakly supervised or knowledge distillation flavored finetuning the training recipe is available on github and according to the authors it can be replicated with 8 a100 gpus and a 600 budget note that this can be competitive with human annotations for example in the self instruct paper the authors found that bootstrapping a model on its own generations can result in performance competitive with instructgpt references sebastian raschka s post on alpaca
