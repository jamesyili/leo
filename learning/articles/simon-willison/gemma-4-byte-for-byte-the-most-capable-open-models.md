# Gemma 4: Byte for byte, the most capable open models

**Source:** https://simonwillison.net/2026/Apr/2/gemma-4/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**[Gemma 4: Byte for byte, the most capable open models](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)**

Four new vision-capable Apache 2.0 licensed reasoning LLMs from Google DeepMind, sized at 2B, 4B, 31B, plus a 26B-A4B Mixture-of-Experts.

Google emphasize "unprecedented level of intelligence-per-parameter", providing yet more evidence that creating small useful models is one of the hottest areas of research right now.

They actually label the two smaller models as E2B and E4B for "Effective" parameter size. The system card explains:

The smaller models incorporate Per-Layer Embeddings (PLE) to maximize parameter efficiency in on-device deployments. Rather than adding more layers or parameters to the model, PLE gives each decoder layer its own small embedding for every token. These embedding tables are large but are only used for quick lookups, which is why the effective parameter count is much smaller than the total.

I don't entirely understand that, but apparently that's what the "E" in E2B means!

One particularly exciting feature of these models is that they are multi-modal beyond just images:

**Vision and audio**: All models natively process video and images, supporting variable resolutions, and excelling at visual tasks like OCR and chart understanding. Additionally, the E2B and E4B models feature native audio input for speech recognition and understanding.

I've not figured out a way to run audio input locally - I don't think that feature is in LM Studio or Ollama yet.

I tried them out using the GGUFs for [LM Studio](https://lmstudio.ai/models/gemma-4). The 2B (4.41GB), 4B (6.33GB) and 26B-A4B (17.99GB) models all worked perfectly, but the 31B (19.89GB) model was broken and spat out `"---\n"` in a loop for every prompt I tried.

The succession of [pelican quality](https://gist.github.com/simonw/12ae4711288637a722fd6bd4b4b56bdb) from 2B to 4B to 26B-A4B is notable:

E2B:

![](https://static.simonwillison.net/static/2026/gemma-4-2b-pelican.png)

E4B:

![](https://static.simonwillison.net/static/2026/gemma-4-4b-pelican.png)

26B-A4B:

![](https://static.simonwillison.net/static/2026/gemma-4-26b-pelican.png)

(This one actually had an SVG error - "error on line 18 at column 88: Attribute x1 redefined" - but after [fixing that](https://gist.github.com/simonw/12ae4711288637a722fd6bd4b4b56bdb?permalink_comment_id=6074105#gistcomment-6074105) I got probably the best pelican I've seen yet from a model that runs on my laptop.)

Google are providing API access to the two larger Gemma models via their [AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemma-4-31b-it). I added support to [llm-gemini](https://github.com/simonw/llm-gemini) and then [ran a pelican](https://gist.github.com/simonw/f9f9e9c34c7cc0ef5325a2876413e51e) through the 31B model using that:

llm -m gemini/gemma-4-31b-it 'Generate an SVG of a pelican riding a bicycle'

Pretty good, though it is missing the front part of the bicycle frame:

![](https://static.simonwillison.net/static/2026/gemma-4-31b-pelican.png)

    
Tags: [google](https://simonwillison.net/tags/google), [ai](https://simonwillison.net/tags/ai), [generative-ai](https://simonwillison.net/tags/generative-ai), [local-llms](https://simonwillison.net/tags/local-llms), [llms](https://simonwillison.net/tags/llms), [llm](https://simonwillison.net/tags/llm), [vision-llms](https://simonwillison.net/tags/vision-llms), [pelican-riding-a-bicycle](https://simonwillison.net/tags/pelican-riding-a-bicycle), [llm-reasoning](https://simonwillison.net/tags/llm-reasoning), [gemma](https://simonwillison.net/tags/gemma), [llm-release](https://simonwillison.net/tags/llm-release), [lm-studio](https://simonwillison.net/tags/lm-studio)
