# Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer

**Source:** https://simonwillison.net/2026/Mar/30/mr-chatterbox/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

Trip Venturella released [Mr. Chatterbox](https://www.estragon.news/mr-chatterbox-or-the-modern-prometheus/), a language model trained entirely on out-of-copyright text from the British Library. Here's how he describes it in [the model card](https://huggingface.co/tventurella/mr_chatterbox_model):

Mr. Chatterbox is a language model trained entirely from scratch on a corpus of over 28,000 Victorian-era British texts published between 1837 and 1899, drawn from a dataset made available [by the British Library](https://huggingface.co/datasets/TheBritishLibrary/blbooks). The model has absolutely no training inputs from after 1899 — the vocabulary and ideas are formed exclusively from nineteenth-century literature.

Mr. Chatterbox's training corpus was 28,035 books, with an estimated 2.93 billion input tokens after filtering. The model has roughly 340 million paramaters, roughly the same size as GPT-2-Medium. The difference is, of course, that unlike GPT-2, Mr. Chatterbox is trained entirely on historical data.

Given how hard it is to train a useful LLM without using vast amounts of scraped, unlicensed data I've been dreaming of a model like this for a couple of years now. What would a model trained on out-of-copyright text be like to chat with?

Thanks to Trip we can now find out for ourselves!

The model itself is tiny, at least by Large Language Model standards - just [2.05GB](https://huggingface.co/tventurella/mr_chatterbox_model/tree/main) on disk. You can try it out using Trip's [HuggingFace Spaces demo](https://huggingface.co/spaces/tventurella/mr_chatterbox):

![Screenshot of a Victorian-themed chatbot interface titled "🎩 Mr. Chatterbox (Beta)" with subtitle "The Victorian Gentleman Chatbot". The conversation shows a user asking "How should I behave at dinner?" with the bot replying "My good fellow, one might presume that such trivialities could not engage your attention during an evening](https://static.simonwillison.net/static/2026/chatterbox.jpg)

Honestly, it's pretty terrible. Talking with it feels more like chatting with a Markov chain than an LLM - the responses may have a delightfully Victorian flavor to them but it's hard to get a response that usefully answers a question.

The [2022 Chinchilla paper](https://arxiv.org/abs/2203.15556) suggests a ratio of 20x the parameter count to training tokens. For a 340m model that would suggest around 7 billion tokens, more than twice the British Library corpus used here. The smallest Qwen 3.5 model is 600m parameters and that model family starts to get interesting at 2b - so my hunch is we would need 4x or more the training data to get something that starts to feel like a useful conversational partner.

But what a fun project!

Running it locally with LLM

I decided to see if I could run the model on my own machine using my [LLM](https://llm.datasette.io/) framework.

I got Claude Code to do most of the work - [here's the transcript](https://gisthost.github.io/?7d0f00e152dd80d617b5e501e4ff025b/index.html).

Trip trained the model using Andrej Karpathy's [nanochat](https://github.com/karpathy/nanochat), so I cloned that project, pulled the model weights and told Claude to build a Python script to run the model. Once we had that working (which ended up needing some extra details from the [Space demo source code](https://huggingface.co/spaces/tventurella/mr_chatterbox/tree/main)) I had Claude [read the LLM plugin tutorial](https://llm.datasette.io/en/stable/plugins/tutorial-model-plugin.html) and build the rest of the plugin.

[llm-mrchatterbox](https://github.com/simonw/llm-mrchatterbox) is the result. Install the plugin like this:

llm install llm-mrchatterbox

The first time you run a prompt it will fetch the 2.05GB model file from Hugging Face. Try that like this:

llm -m mrchatterbox "Good day, sir"

Or start an ongoing chat session like this:

llm chat -m mrchatterbox

If you don't have LLM installed you can still get a chat session started from scratch using uvx like this:

uvx --with llm-mrchatterbox llm chat -m mrchatterbox

When you are finished with the model you can delete the cached file using:

llm mrchatterbox delete-model

This is the first time I've had Claude Code build a full LLM model plugin from scratch and it worked really well. I expect I'll be using this method again in the future.

I continue to hope we can get a useful model from entirely public domain data. The fact that Trip was able to get this far using nanochat and 2.93 billion training tokens is a promising start.

**Update 31st March 2026**: I had missed this when I first published this piece but Trip has his own [detailed writeup of the project](https://www.estragon.news/mr-chatterbox-or-the-modern-prometheus/) which goes into much more detail about how he trained the model. Here's how the books were filtered for pre-training:

First, I downloaded the British Library dataset split of all 19th-century books. I filtered those down to books contemporaneous with the reign of Queen Victoria—which, unfortunately, cut out the novels of Jane Austen—and further filtered those down to a set of books with a optical character recognition (OCR) confidence of .65 or above, as listed in the metadata. This left me with 28,035 books, or roughly 2.93 billion tokes for pretraining data.

Getting it to behave like a conversational model was a lot harder. Trip started by trying to train on plays by Oscar Wilde and George Bernard Shaw, but found they didn't provide enough pairs. Then he tried extracting dialogue pairs from the books themselves with poor results. The approach that worked was to have Claude Haiku and GPT-4o-mini generate synthetic conversation pairs for the supervised fine tuning, which solved the problem but sadly I think dilutes the "no training inputs from after 1899" claim from the original model card.

    
        
Tags: [ai](https://simonwillison.net/tags/ai), [andrej-karpathy](https://simonwillison.net/tags/andrej-karpathy), [generative-ai](https://simonwillison.net/tags/generative-ai), [local-llms](https://simonwillison.net/tags/local-llms), [llms](https://simonwillison.net/tags/llms), [ai-assisted-programming](https://simonwillison.net/tags/ai-assisted-programming), [hugging-face](https://simonwillison.net/tags/hugging-face), [llm](https://simonwillison.net/tags/llm), [training-data](https://simonwillison.net/tags/training-data), [uv](https://simonwillison.net/tags/uv), [ai-ethics](https://simonwillison.net/tags/ai-ethics), [claude-code](https://simonwillison.net/tags/claude-code)
