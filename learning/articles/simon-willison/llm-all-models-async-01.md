# llm-all-models-async 0.1

**Source:** https://simonwillison.net/2026/Mar/31/llm-all-models-async/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**Release:** [llm-all-models-async 0.1](https://github.com/simonw/llm-all-models-async/releases/tag/0.1)

    
LLM plugins can define new models in both [sync](https://llm.datasette.io/en/stable/plugins/tutorial-model-plugin.html) and [async](https://llm.datasette.io/en/stable/plugins/advanced-model-plugins.html#async-models) varieties. The async variants are most common for API-backed models - sync variants tend to be things that run the model directly within the plugin.

My [llm-mrchatterbox](https://simonwillison.net/2026/Mar/30/mr-chatterbox/#running-it-locally-with-llm) plugin is sync only. I wanted to try it out with various Datasette LLM features (specifically [datasette-enrichments-llm](https://github.com/datasette/datasette-enrichments-llm)) but Datasette can only use async models.

So... I had Claude spin up this plugin that turns sync models into async models using a thread pool. This ended up needing an extra plugin hook mechanism in LLM itself, which I shipped just now in [LLM 0.30](https://llm.datasette.io/en/stable/changelog.html#v0-30).

    
        
Tags: [llm](https://simonwillison.net/tags/llm), [async](https://simonwillison.net/tags/async), [python](https://simonwillison.net/tags/python)
