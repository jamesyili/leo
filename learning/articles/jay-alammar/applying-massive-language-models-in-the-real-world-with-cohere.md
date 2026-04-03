# Applying massive language models in the real world with Cohere

**Source:** http://jalammar.github.io/applying-large-language-models-cohere/
**Ingested:** 2026-04-02
**Tags:** ml-fundamentals, visual-explanations

---

A little less than a year ago, I joined the awesome [Cohere](https://cohere.ai) team. The company trains massive language models (both GPT-like and BERT-like) and offers them as an API (which also supports finetuning). Its founders include Google Brain alums including co-authors of the original Transformers paper. It’s a fascinating role where I get to help companies and developers put these massive models to work solving real-world problems.

I love that I get to share some of the intuitions developers need to start problem-solving with these models. Even though I’ve been working very closely on pretrained Transformers for the past several years (for this blog and in developing [Ecco](https://github.com/jalammar/ecco)), I’m enjoying the convenience of problem-solving with managed language models as it frees up the restrictions of model loading/deployment and memory/GPU management.

These are some of the articles I wrote and collaborated on with colleagues over the last few months:

[Intro to Large Language Models with Cohere](https://docs.cohere.ai/intro-to-llms/)

    

  [![](https://files.readme.io/0a9715d-IntroToLLM_Visual_1.svg)](https://docs.cohere.ai/intro-to-llms/)
    

    

    
This is a high-level intro to large language models to people who are new to them. It establishes the difference between generative (GPT-like) and representation (BERT-like) models and examples use cases for them.

    
This is one of the first articles I got to write. It's extracted from a much larger document that I wrote to explore some of the visual language to use in explaining the application of these models.

    

[A visual guide to prompt engineering ](https://docs.cohere.ai/prompt-engineering-wiki/)

    

  [![](https://files.readme.io/db285b8-PromptEngineering_Visual_2.svg)](https://docs.cohere.ai/prompt-engineering-wiki/)
    

    

        
Massive GPT models open the door for a new way of programming. If you structure the input text in the right way, you can useful (and often fascinating) results for a lot of taasks (e.g. text classification, copy writing, summarization...etc).
        

        
This article visually demonstrates four principals to create prompts effectively. 

    

[ Text Summarization](https://docs.cohere.ai/text-summarization-example/)

    

  [![](https://files.readme.io/296454c-TextSummarization_Visual_1.svg)](https://docs.cohere.ai/text-summarization-example/)
    

    

    
This is a walkthrough of creating a simple summarization system. It links to a jupyter notebook which includes the code to start experimenting with text generation and summarization.

    
The end of this notebook shows an important idea I want to spend more time on in the future. That of how to rank/filter/select the best from amongst multiple generations.

    

[Semantic Search](https://docs.cohere.ai/semantic-search/)

    

  [![](https://files.readme.io/4ec00e1-SemanticSearch_Visual_1.svg)](https://docs.cohere.ai/semantic-search/)
    

    

    
Semantic search has to be one of the most exciting applications of sentence embedding models. This tutorials implements a "similar questions" functionality using sentence embeddings and a a vector search library.

    
The vector search library used here is [Annoy](https://github.com/spotify/annoy) from Spotify. There are a bunch of others out there. [Faiss](https://github.com/facebookresearch/faiss) is used widely. I experiment with [PyNNDescent](https://github.com/lmcinnes/pynndescent) as well.

    

[ Finetuning Representation Models](https://docs.cohere.ai/finetuning-representation-models/)

    

  [![](https://files.readme.io/699aead-TrainingRepModels_Visual_4.svg)](https://docs.cohere.ai/docs/training-a-representation-model)
    

    

    
Finetuning tends to lead to the best results language models can achieve. This article explains the intuitions around finetuning representation/sentence embedding models. I've added a couple more visuals to the [Twitter thread](https://twitter.com/JayAlammar/status/1490712428686024705).

The research around this area is very interesting. I've highly enjoyed papers like [Sentence BERT](https://arxiv.org/abs/1908.10084) and [Approximate Nearest Neighbor Negative Contrastive Learning for Dense Text Retrieval](https://arxiv.org/abs/2007.00808)

    

[Controlling Generation with top-k & top-p](https://docs.cohere.ai/token-picking/)

    

  [![](https://files.readme.io/ab291f6-Top-KTop-P_Visual_4.svg)](https://docs.cohere.ai/token-picking/)
    

    

        
This one is a little bit more technical. It explains the parameters you tweak to adjust a GPT's *decoding strategy* -- the method with which the system picks output tokens. 
        

    

[Text Classification Using Embeddings](https://docs.cohere.ai/text-classification-embeddings/)

    

  [![](https://files.readme.io/ee56264-Controlling_Generation_with_Top-K__Top-P_Visual_1.svg)](https://docs.cohere.ai/text-classification-embeddings/)
    

    

        

        This is a walkthrough of one of the most common use cases of embedding models -- text classification. It is similar to [A Visual Guide to Using BERT for the First Time](http://127.0.0.1:4000/a-visual-guide-to-using-bert-for-the-first-time/), but uses Cohere's API.
        

    

You can find these and upcoming articles in the [Cohere docs](https://docs.cohere.ai/) and [notebooks repo](https://github.com/cohere-ai/notebooks). I have quite number of experiments and interesting workflows I’d love to be sharing in the coming weeks. So stay tuned!
