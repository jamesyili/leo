# A Guide for Debugging LLM Training Data

**Source:** https://cameronrwolfe.substack.com/p/llm-debugging
**Ingested:** 2026-04-02
**Tags:** llms, rlhf, architectures

---

![](https://substackcdn.com/image/fetch/$s_!EX0M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37c17277-3f8e-4ff3-8e90-2dd7c2bb5565_2516x1357.png)

(from [2])

Most discussions of LLM training focus heavily on models and algorithms. We enjoy experimenting with new frameworks like [GRPO](https://arxiv.org/abs/2402.03300) and anticipate the release of next-generation models like [Gemma-3](https://arxiv.org/abs/2503.19786) and [Qwen-3](https://arxiv.org/abs/2505.09388). However, the primary factor distinguishing success from failure in LLM training is the quality of the training dataset. Unfortunately, this topic receives far less attention compared to other popular research areas. In this overview, we will offer a data-centric guide to debugging and optimizing LLM training, *emphasizing practical strategies that we can use to iteratively enhance our data and develop more powerful LLMs*.

The LLM Development Lifecycle

![](https://substackcdn.com/image/fetch/$s_!xSnb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa43347c-41d6-473e-8a46-095192476264_1934x682.png)

The key steps of LLM development

When training an LLM, we follow an iterative and empirically-driven process that is comprised of two primary steps (shown above):

Training an LLM.

Evaluating the LLM.

To develop an LLM, we simply repeat these steps, eventually yielding an LLM that performs well on evaluations relevant to our application of interest. 

**LLM evaluation.** We will not discuss the topic of evaluating LLMs in detail, as this topic is extremely complex. At a high level, however, we evaluate an LLM in two ways—*either manually (i.e., with humans) or automatically*. Human evaluation can be setup in several ways; e.g., picking the better of two model responses or scoring a model response along several quality dimensions; see below. As with any other data annotation project, we must invest effort to make sure that these [human evaluations are high-quality](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/) and align with what we are trying to measure. 

![](https://substackcdn.com/image/fetch/$s_!hAhC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f6ef46e-8ff1-4af4-96df-f4c08514ddf7_2486x742.png)

(from [5, 12])

When developing an LLM, human evaluation is the gold standard for measuring quality—*we should always depend on human evaluation to provide a definitive signal of whether our LLM is getting better or not*. However, human evaluation is also time intensive (i.e., takes several days or weeks)! To avoid slowing down our iteration speed, we must develop automatic evaluation metrics to provide a more efficient proxy measure of model quality. Using these automatic metrics, we can perform a much larger number of model iterations between each human evaluation trial, allowing us to improve model quality more quickly; see below. 

![](https://substackcdn.com/image/fetch/$s_!rRSF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37f8440c-a1aa-4252-af9f-e8047f7dcf09_1354x654.png)

In terms of automatic evaluation, two main techniques that are typically used—*benchmark-style evaluation and LLM judges*; see below. These two strategies test the model’s performance on closed and open-ended tasks, respectively. 

![](https://substackcdn.com/image/fetch/$s_!FCJd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00b3ca29-cb6d-472e-b4f4-69ad7875d503_938x418.png)

([source](https://www.databricks.com/blog/limit-less-more-instruction-tuning))

Benchmark-style evaluations (e.g., multiple-choice style questions or question-answer pairs) have been used throughout the history of NLP research. Modern examples of such benchmarks for LLMs include [MMLU](https://arxiv.org/abs/2009.03300) or [GPQA Diamond](https://arxiv.org/abs/2311.12022). These benchmarks have closed-ended solutions, but LLMs produce open-ended outputs that can be difficult to evaluate. The most popular technique for open-ended evaluation is LLM-as-a-Judge, or other related techniques (e.g., [reward models](https://arxiv.org/abs/2403.13787), [finetuned judges](https://cameronrwolfe.substack.com/p/finetuned-judge) or [verifiers](https://arxiv.org/abs/2408.15240)); see the article below for details. 

**Tweaking the data.** Once we have an evaluation setup, we can begin to train new models and measure their performance. For each new model, we perform some intervention that will (hopefully) benefit the LLM’s performance. Traditionally, AI researchers are very interested in algorithms and architectures[1](#footnote-1), and sometimes we do tweak these details! For example, Llama 4 made significant changes to its post-training pipeline[2](#footnote-2), and many LLMs are incorporating new algorithms—*such as [RLVR](https://arxiv.org/abs/2411.15124)*—into their training pipelines to improve reasoning capabilities. Despite these recent developments, however, *the majority of interventions are data-related*. We tweak our training data, leave everything else fixed, retrain (or keep training) our model, and see if the new data improves the model’s performance. 

![](https://substackcdn.com/image/fetch/$s_!XUX1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24592711-8eae-4089-a3e2-2299479d1fcf_1644x764.png)

(from [2])

The most conceptually straightforward data intervention is just collecting more training data. Collecting more data as an LLM is being developed is common. For example, the Llama 2 report [3] notes that models are post-trained in several stages, where more data is collected for further post-training at each stage; see above. Collecting data might seem simple conceptually, but data annotation is an incredibly complex and nuanced topic that requires the correct strategy—*and usually prior experience*—to execute successfully; see [here](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/) and [here](https://eugeneyan.com/writing/labeling-guidelines/) for more details.

*“Getting the most out of human data involves iterative training of models, evolving and highly detailed data instructions, translating through data foundry businesses, and other challenges that add up.”* - [RLHF book](https://rlhfbook.com/c/06-preference-data.html)

**Curating data.** In this report, we will not focus on collecting more data. Instead, we will focus on curating (or debugging) the data we have available. This is an orthogonal approach to human data collection; see below. To do this, we use a variety of techniques to identify high or low-quality data so that we can fix issues in our dataset and focus the training process on the highest-quality data.

![](https://substackcdn.com/image/fetch/$s_!2flt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a8502ae-348d-47be-bd17-888dceb16c60_1598x826.png)

Two directions to approaching high-quality data ([source](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/))

Given that most interventions to LLM quality are data-related, data curation is a pivotally important topic; e.g., there are [several](https://www.datologyai.com/) [startups](https://github.com/bespokelabsai/curator) and a [swath](https://arxiv.org/abs/2305.11206) [of](https://arxiv.org/abs/2406.03476) [great](https://arxiv.org/abs/2502.03387) [papers](https://arxiv.org/abs/2305.13169) focused on this topic. Despite being so fundamental to the LLM training process, however, data-related topics are usually underrepresented in AI research. Optimizing data is simply not a flashy or popular topic, *but it is more often than not the key differentiator between success and failure when training LLMs.*

How do we curate data?

Put simply, there are two ways we can curate data:

Directly looking at the data.

Using model outputs to debug the training data. 

For example, we can curate and debug our data via manual inspection or basic searches and heuristics. Additionally, we can use another model to analyze our data; e.g., tagging, classification, assigning a quality score and more. All of these strategies are unrelated to the downstream model we are creating—*we are directly looking at the training data*. Once we have trained a model, however, we can further fuel the data curation process by debugging the LLM’s outputs as follows:

Identifying poor model outputs.

Finding data issues that (potentially) contributed to these outputs. 

Fixing the data via some intervention.

Re-training the model.

**A strategy for debugging.** In this overview, we will refer to the two strategies outlined above as data and model-focused curation. There are many terms one could use to refer to these ideas, and this nomenclature is definitely not perfect; e.g., data-focused curation can still involve the use of a model, we just use models to analyze data instead of using the data to train a model. However, we will use this terminology throughout to keep our discussion clear and consistent. 

![](https://substackcdn.com/image/fetch/$s_!80-H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefd00ea7-16a3-49ba-9cd8-de68803dc606_1596x376.png)

As we discuss these ideas, we should keep in mind that data and model-focused debugging are **NOT** mutually exclusive. In fact, we should almost always leverage them both. Data-focused curation does not require training any models, which is incredibly useful in the early stages of LLM development. *Experienced scientists spend a lot of time analyzing and understanding their data prior to doing any modeling*. 

We continue to perform such data-focused analysis over time, but new avenues of analysis become possible once we’ve trained a model. To debug and improve our LLM, we must develop a multi-faceted approach that allows us to gain a deeper understanding of our model, our data and the connection between them.

Data-Focused Curation: Looking at the Data

To gain a deep understanding of our data, we will start by simply looking at our data manually. As we manually inspect data, we will begin to notice—*and fix in some cases*—important issues and patterns in our data. To scale this curation process beyond our own judgement, however, we will need to use automated techniques based either upon heuristics or other machine learning models. 

![](https://substackcdn.com/image/fetch/$s_!O22R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e974e72-5226-4ece-8f07-f7f41f7b11c9_1166x356.png)

([source](https://x.com/gdb/status/1622683988736479232))

**Manual inspection.** The first step in debugging an LLM is simply looking at the model’s training data. *This should occur before we begin to train any models and should continue throughout the lifetime of model development*. Manual data inspection is very time consuming (and not always the most fun!), but it is an important part of LLM development. By taking time to manually inspect the data, we gain a better understanding of this data and, in turn, a better understanding of our model. If you ask any LLM researcher, they will likely confirm that they spend a large portion of their time manually inspecting data. This unpopular activity is a key contributor to success in training LLMs—*it cannot (and should not) be avoided*! 

![](https://substackcdn.com/image/fetch/$s_!jw1l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5bc4f6c-d99c-404c-a61c-2fa78071066c_685x500.png)

Original credit goes to [@code_star](https://x.com/code_star) for this hilarious (and accurate) meme

The main limitation of manual data inspection is the simple fact that it is not scalable—*there is only so much data that we as researchers can manually inspect*. Once we have performed enough manual inspection[3](#footnote-3) to understand our data well, we need to develop better strategies for scaling our data inspection efforts. 

**Heuristic filtering.** Manual inspection will uncover many issues and interesting patterns in our data. For example, we might notice that certain words are re-used very frequently; see below. To make sure our model does not reflect these sub-optimal patterns in the data, we can use heuristics to find training examples that match these patterns and filter (or modify) them. For example, finding data that re-uses the same set of words can be done via a simple string match. Here, we are using basic heuristics to solve noticeable limitations in our data. 

![](https://substackcdn.com/image/fetch/$s_!OEJA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd86002e5-2eda-44be-a4fe-ecea571daa10_1604x916.png)

([source](https://www.reddit.com/r/ClaudeAI/comments/1fyk8ql/claude_ignores_its_own_system_prompts_with/))

There are many other heuristics for data inspection and filtering that we might consider. For example, we might notice that certain sources of data are of higher quality or have useful properties compared to other data sources. To act on this, we can emphasize this data during training[4](#footnote-4) or even obtain more data from this source. Similarly, we might notice a formatting issue in a subset of our data that can be identified or fixed with a regex statement. Depending on our observations during the manual inspection phase, there are an almost infinite number of heuristic checks or fixes that might need to be applied to our training dataset.

**Model-based filtering.** If observed issues cannot be fixed heuristically, then we can fix them with the help of a machine learning model. [fastText classifiers](https://github.com/facebookresearch/fastText) are heavily used for LLM data filtering due to their efficiency—*they can operate even at pretraining scale*. Concrete examples of fastText models being used for LLM data filtering include language identification (e.g., filtering out non-English data) or [identifying toxic content](https://arxiv.org/abs/2402.00159). However, [custom fastText models can be easily trained](https://fasttext.cc/docs/en/python-module.html) to handle a variety of bespoke filtering tasks. We just *i)* train the model on examples of the data we want to identify, *ii)* use the model to identify such data and *iii)* either remove or keep the data that is identified; see below.

![](https://substackcdn.com/image/fetch/$s_!OCL8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffef41e5d-d721-460b-97c1-78d9cd3baaed_2048x731.png)

([source](https://docs.google.com/presentation/d/179dpzWSQ9G7EAUlvaJdeE0av9PLuk9Rl33nfhHSJ4xI/edit?usp=sharing))

We can also use other kinds of models for the purpose of data filtering. For example, [LLM-as-a-Judge](https://cameronrwolfe.substack.com/p/llm-as-a-judge)-style models are commonly used both for filtering data and creating synthetic data. [Constitutional AI](https://arxiv.org/pdf/2212.08073) is a popular example of using LLM judges to create synthetic preference pairs and Llama 4 uses an LLM judge to remove easier examples from their [supervised finetuning](https://cameronrwolfe.substack.com/p/understanding-and-using-supervised) dataset. We can apply similar approaches to identify arbitrary properties and patterns—*usually with reasonably-high accuracy*—within our data for the purpose of filtering. 

*“We removed more than 50% of our data tagged as easy by using Llama models as a judge and did lightweight SFT on the remaining harder set.”* - from [13]

Such larger models are much less efficient relative to a fastText model, which limits them to smaller-scale use cases (usually post-training). If we compare [BERT-base](https://cameronrwolfe.substack.com/p/language-understanding-with-bert), which is ~10,000× smaller than some of the largest modern LLMs, to a fastText model, the difference in efficiency and required hardware is massive; see below. Nonetheless, developing more sophisticated approaches and models for data curation is one of the most impactful topics in AI research right now. 

![](https://substackcdn.com/image/fetch/$s_!hcuw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74956760-c648-499a-8c96-b6b9e8d2d027_1694x648.png)

Using fastText vs. BERT-base for data filtering ([source](https://docs.google.com/presentation/d/179dpzWSQ9G7EAUlvaJdeE0av9PLuk9Rl33nfhHSJ4xI/edit?usp=sharing))

Model-Focused Curation: Debugging the LLM’s Outputs

Once we have started training LLMs over our data, we can begin to use these LLMs to debug issues within the training dataset. The idea of model-focused curation is simple, we just:

Identify problematic or incorrect outputs produced by our model.

Search for instances of training data that may lead to these outputs.

The identification of problematic outputs is handled through our evaluation system. We can either have humans (even ourselves!) identify poor outputs via manual inspection or efficiently find incorrect or low-scoring outputs via our automatic evaluation setup. Once these problematic outputs have been identified, debugging our LLM becomes a search problem—*we want to find training examples that may be related to these poor outputs*. In this section, we will go over several common approaches for this, culminating with a low-cost and efficient method for tracing data called OLMoTrace [2] that was recently developed by Ai2. 

Searching over Training Data

![](https://substackcdn.com/image/fetch/$s_!3e1n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F407d89cc-a925-4b68-9d9b-5c0a2f563fec_1654x516.png)

Searching for relevant training data is similar to any other search problem; see above. The only difference is that our query is an output from our LLM, rather than something that we input into a search bar. But, all of the same techniques for search can be applied to solving this problem. For a deep dive on this topic, check out the overview below. In this section, we will briefly cover the key concepts of search and how they can be applied to tracing training data.

**Lexical search.** For many years prior to the popularization of deep learning, most search engines were [purely lexical](https://huggingface.co/blog/xhluca/bm25s), meaning that they rely on keyword (or n-gram) matches to find documents relevant to a query. To find these matches efficiently, we use a data structure called an [inverted index](https://www.geeksforgeeks.org/inverted-index/). By counting matches between each query and document, as well as considering the uniqueness of each n-gram that is matched, we can derive a relevance score for each document. The most common algorithm for this is [BM25](https://en.wikipedia.org/wiki/Okapi_BM25), which is computed as shown below.

![](https://substackcdn.com/image/fetch/$s_!5f9T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82315c90-36c0-46e7-92b9-7b77a34a5280_2250x644.png)

Equation for computing BM25 scores

Although these details might seem complex, we can easily implement BM25-powered search via Python packages like [rank_bm25](https://github.com/dorianbrown/rank_bm25) or [bm25s](https://github.com/xhluca/bm25s). With these packages, we can build a search index over our data in Python and start running searches as shown in the code example below. As we can see, this functionality is easy to prototype and begin using without too much effort!

from transformers import AutoTokenizer
from rank_bm25 import BM25Okapi

tok = AutoTokenizer.from_pretrained(<your tokenizer>)

corpus = [
    "Here is a training example",
    "Here is another training example...",
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

**Semantic search.** Despite the power and efficiency of lexical search, this technique is still dependent upon keyword matching—*semantic matches (i.e., different words with similar meaning) are not captured by this framework*. If we want to handle semantic matches, we need to use some form of vector search; see below.

![](https://substackcdn.com/image/fetch/$s_!pf1M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd19f706e-65a8-4236-a652-d1bd5958e61c_2124x358.png)

A simple vector search pipeline

In vector search, we use an [embedding model](https://stackoverflow.blog/2023/11/09/an-intuitive-introduction-to-text-embeddings/) to produce and embedding for each document we want to search. Then, we store all of these embeddings in a vector database, which allows us to efficiently search for similar embeddings using algorithms like [hierarchical navigable small worlds (HNSW)](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world). From here, we can simply embed our query and search for similar embeddings within the index, allowing us to find documents that are semantically similar to our query! This is exactly what is done by retrieval augmented generation (RAG) to retrieve relevant text chunks to add into the context of an LLM; see [here](https://cameronrwolfe.substack.com/p/a-practitioners-guide-to-retrieval) for details. 

![](https://substackcdn.com/image/fetch/$s_!qHxF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F635a986a-9e9a-4a3a-8fd8-860017df9770_1802x786.png)

Difference between bi-encoders and cross-encoders

The semantic search system outlined above uses bi-encoders, which produce separate embeddings—*that are matched together via [cosine similarity scores](https://www.geeksforgeeks.org/cosine-similarity/)*—for each document and query. However, we can also use cross-encoders, which take both the document and query as input and output a single similarity score. The difference between these two strategies is illustrated in the figure above. A variety of pretrained bi-encoders and cross-encoders are available in public repos and can be either finetuned or used out-of-the-box; see [here](https://sbert.net/) for more details. 

Modern search systems combine all of these techniques. A hybrid of both bi-encoders and (BM25) lexical search are first used to efficiently retrieve documents that are most relevant to our query. Then, we perform a fine-grained ranking of retrieved documents using a cross-encoder, *bringing the most relevant documents to the top of the list*; see below. All of these components can be finetuned over data collected as the search engine is used to improve their accuracy over time.

![](https://substackcdn.com/image/fetch/$s_!Alf3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb72ab1d3-a9ee-42ea-ba81-8e03fa5f841e_1720x446.png)

Modern AI-powered search framework

**Applying search to debugging.** Now that we understand the basics of search systems, we can also apply these ideas to debugging LLM outputs. However, there are two unique considerations for debugging LLM outputs that make this use case different from a standard search application:

LLM training datasets can be massive (tens of trillions of tokens), which can prohibit the use of some techniques.

Depending on the use case, the output of an LLM, as well as the documents over which the LLM is trained, can be very long.

If we are tracing a large dataset, using techniques like vector search—*although not impossible*—can be both time consuming and expensive. We have to first produce embeddings for our entire dataset, then store these embeddings in a vector database to make them searchable. This process requires a lot of setup (including the creation of large-scale data pipelines!), which makes the barrier to entry high. 

Going further, the fact that our LLM’s outputs and training documents can be very long means that we need to approach this search problem differently. Instead of using the entire output as a search query, we need to consider shorter spans in this output and search for similar spans in the training data. Ideally, we want to develop a technique for tracing our training data that is:

Relatively simple to setup.

Efficient on large-scale datasets. 

Able to operate on a (shorter) span level.

[Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens](https://arxiv.org/abs/2401.17377) [1]

*“Instead of pre-computing n-gram count tables (which would be very expensive), we develop an engine named infini-gram—powered by suffix arrays—that can compute ∞-gram (as well as n-gram with arbitrary n) probabilities with millisecond-level latency.”* - from [1]

To understand how we can efficiently trace a massive dataset, we need to first understand the concept of an infini-gram [1]. Put simply, infini-grams are the generalization of [n-grams](https://en.wikipedia.org/wiki/N-gram) to arbitrarily large values of `N`. As we will see, the data structure that we use to compute the probability of an infini-gram can also be used to (very efficiently) locate and count text spans of arbitrary length within a massive dataset. *This property is very useful for model-focused curation and debugging!*

![](https://substackcdn.com/image/fetch/$s_!v-fq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8879a41a-9544-4403-b544-0b66338a90be_2000x838.png)

Creating n-grams from a sequence of text

**What are n-gram LMs? **An n-gram is simply an ordered set of `N` tokens (or words). Given a sequence of text, we can break it into n-grams as shown above, where we choose `N = 3`. If we break an entire dataset of text into n-grams, we can actually compute the probability of a given n-gram by simply counting the number of times that it occurs within the dataset; see below.

![](https://substackcdn.com/image/fetch/$s_!ouM8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a6e7f4c-5367-4a52-a0e7-53de8f0b45f6_2366x622.png)

Computing n-gram probabilities

All of these counts are usually pre-computed and stored in a [count table](https://web.stanford.edu/~jurafsky/slp3/3.pdf), allowing us to quickly lookup n-gram probabilities and evaluate the expression shown above. We can actually form a simple language model using n-gram probabilities! To predict the next token in a sequence using n-grams, we just:

Look at the last `N - 1` tokens in the sequence.

Get the probability of each possible n-gram given the prior `N - 1` tokens.

[Sample the next token](https://huggingface.co/blog/mlabonne/decoding-strategies) similarly to any other language model. 

**Limitations of n-grams.** Practically speaking, n-gram LMs are not great at generating text—*you will not be able to make a powerful chatbot by counting n-grams*. Although this is true for any value of `N`, one of the key issues that limits the performance of n-gram LMs is the fact that n-gram count tables grow (almost) exponentially in size with respect to `N`. As a result, most n-gram LMs are limited to small values of `N`—*e.g., *`N = 5`* is a common setting*—and have a low capacity for capturing meaningful, long-context language distributions; see below. 

![](https://substackcdn.com/image/fetch/$s_!nLAq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2286afc0-b048-419f-95f1-2e152ff94137_1884x942.png)

(from [1])

Additionally, n-gram LMs struggle with sparsity. Some n-grams may not appear in our data, forcing us to fall back to smaller n-grams to compute a probability—*this concept is typically referred to as n-gram “backoff”*. Forming a valid probability estimate when backing off to smaller n-grams is actually [quite complicated](https://en.wikipedia.org/wiki/Katz%27s_back-off_model). 

**Making n-grams relevant again.** In [1], authors propose a variant of n-gram LMs—*called infini-grams (or ∞-grams)*—that mesh better with modern LLMs. Relative to standard n-grams, infini-grams make two key changes:

They are trained over a massive text dataset (trillions of tokens) like any other modern LLM, thus mitigating issues with sparsity.

The value of `N` can be made arbitrarily large when computing the probability of an n-gram, which captures more meaningful distributions in the data.

**What are ∞-grams?** By making these changes, infini-grams solve the two biggest issues with n-gram LMs that we covered above. *How does this work?* Assume we have a textual sequence `w`. To compute the infini-gram of token `i`, we consider all tokens that precede token `i` in the sequence; see below.

![](https://substackcdn.com/image/fetch/$s_!2kGf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2004290-7717-47cd-896a-46acc539811f_1882x698.png)

Computing infini-gram probabilities

On the left side of this equation, the infini-gram probability is conditioned on the entire prior context of the sequence, which is different from before. However, the right side of this equation exactly matches that of the n-gram probability! *The key difference between n-grams and infini-grams lies in how we select the value of *`N`.

For n-grams, `N` is a (fixed) hyperparameter. In contrast, infini-grams use a backoff procedure to dynamically select `N`. More specifically, we test the denominator of this expression with the largest possible `N`—*all preceding tokens in the sequence*—and continually decrease `N` by one until the denominator is non-zero; see below. 

*“We stop backing off as soon as the denominator becomes positive, upon which the numerator might still be zero… the effective n is equal to one plus the length of the prompt’s longest suffix that appears in the training data.”* - from [1]

If we define `w’`as the subsequence of `w` up to (and including) token `i - 1`, then this backoff procedure is simply finding the longest suffix of `w’` that exists in our dataset. From here, we use the value of `N` found via backoff to compute the infini-gram probability using the standard n-gram probability expression from before.

**Computing ∞-gram probabilities.** To compute infini-gram probabilities, we cannot just precompute counts and store them in a table like before. The value of `N` is unbounded and infini-grams are trained over LLM-scale datasets in [1]—*the size of such a count table would be massive*. Instead, we use a data structure called a [suffix array](https://en.wikipedia.org/wiki/Suffix_array) to create an engine for efficiently computing infini-gram probabilities.

![](https://substackcdn.com/image/fetch/$s_!nERk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F069cd044-9bb4-4bcf-bb11-511d82c54341_729x583.png)

Suffix array on a toy sequence of six characters (from [1])

The concept of a suffix array is depicted above. Given a sequence of text `w` with length `L`, a suffix array is constructed by:

Extracting every suffix of this sequence (there are `L` of them).

Sorting the suffixes [lexicographically](https://en.wikipedia.org/wiki/Lexicographic_order)[5](#footnote-5).

Storing the original index (prior to sorting) of each sorted suffix within a list—*this is the suffix array*!

Consider `w’` to be an arbitrary subarray of `w` running from token `i` to token `j`, where `i < j`.  Any suffix that begins with `w’` is stored consecutively in the suffix array due to the array being sorted lexicographically. Using this property, we can efficiently compute the count of `w’` in `w`. We just find the index of the first and last suffix in the array for which `w’` is a prefix, and the count of `w’` in `w` is the difference between these two indices. If we can compute the count of `w’`, we can compute arbitrary infini-gram probabilities—*this operation can be used to find *`N`* and compute both counts within the infini-gram probability expression*!

![](https://substackcdn.com/image/fetch/$s_!kw-x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d05a53-38fd-4c7d-a477-0b8bd256443d_1053x575.png)

Suffix array on textual tokens (from [1])

**∞-grams for LLMs.** In the context of LLMs, our sequence `w` is the LLM’s entire tokenized training dataset, where document boundaries are marked with fixed separator token(s)[6](#footnote-6); see above. This sequence will be large—*modern LLMs are trained on tens of trillion of tokens*—but suffix arrays can handle data of this scale[7](#footnote-7).

*“During inference, the entire infini-gram index can stay on-disk, which minimizes the compute resources needed (no GPU, and minimal CPU / RAM)… Our most optimized infini-gram engine can count a given n-gram with an average latency of less than 20 milliseconds. It can compute the probability and next-token distribution in 40 milliseconds for n-gram LMs, and in 200 milliseconds for the ∞-gram.”* - from [1]

For example, the suffix array built over a 5T token dataset in [1] consumes ~35Tb of memory. Building this suffix array takes ~48 hours, and the entire suffix array can be stored on disk—*even when computing infini-gram probabilties*—after it is created. The resulting infini-gram engine can be used to compute probabilities for over two *quadrillion* unique n-grams. However, retrieving the count of a given n-gram on a dataset of this size still takes only ~20 milliseconds!

**Using ∞-grams in practice. **Fully grasping the ideas behind infini-grams will take some time. Luckily, the entire infini-gram project—*similarly to any other project from [Ai2](https://allenai.org/)*—is fully open-source! There are plenty of open-source tools available for working with infini-grams in Python. See the [project website](https://infini-gram.io/) for full details. 

%pip install infini_gram 
python -m infini_gram.indexing 
    --data_dir <path to data>
    --save_dir <path to save index>
    --tokenizer llama  # also supports gpt2 and olmo
    --cpus <cpus available>
    --mem <memory available (in Gb)>
    --shards 1  # increase if N > 500B
    --add_metadata 
    --ulimit 1048576

The tool that is most relevant to this overview is the [inifini-gram Python package](https://infini-gram.readthedocs.io/en/latest/pkg.html). Several open LLM training datasets have already been [pre-indexed within this package](https://infini-gram.readthedocs.io/en/latest/pkg.html#pre-built-indexes), but we can also use the package to build an infini-gram index over our custom dataset using the command above. Once the index is available, we can use the infini-gram Python package to efficiently run a variety of different search and counting operations; see below for examples and [here](https://infini-gram.readthedocs.io/en/latest/pkg.html#query-types) for more details. 

from infini_gram.engine import InfiniGramEngine
from transformers import AutoTokenizer

# instantiate tokenizer (must match tokenizer used for indexing)
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    add_bos_token=False,
    add_eos_token=False,
)

# connect to infini-gram engine
engine = InfiniGramEngine(
    index_dir=<path to index>,
    eos_token_id=tokenizer.eos_token_id,
)

# sample n-gram / sequence
inp = "This is my sample n-gram sequence."
inp_ids = tokenizer.encode(inp)

# find matching n-grams in dataset
result = engine.find(input_ids=input_ids)

# n-gram count
result = engine.count(input_ids=inp_ids)

# n-gram probability
result = engine.prob(
    prompt_ids=inp_ids[:-1],
    cont_id=inp_ids[-1],
)

# next token distribution
result = engine.ntd(prompt_ids=inp_ids)

# infini-gram probability
result = engine.infgram_prob(
    prompt_ids=inp_ids[:-1],
    cont_id=inp_ids[-1],
)

[OLMoTrace: Tracing Language Model Outputs Back to Trillions of Training Tokens](https://arxiv.org/abs/2504.07096) [2]

![](https://substackcdn.com/image/fetch/$s_!sFmj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5aedfd0f-700f-41bd-85b3-3eff8c3ae7dd_1232x810.png)

(from [2])

OLMoTrace [2] pioneers a novel approach for efficiently attributing the output of an LLM to examples within its training data. This approach is deployed within the [Ai2 playground](https://playground.allenai.org/) (shown above) and can perform a trace to retrieve training documents that are relevant to an LLM’s output in seconds. Given that LLMs are trained over massive datasets, we might wonder how such a real-time trace would be possible. Luckily, we have already learned the answer: *infini-grams*! 

*“The purpose of OLMOTRACE is to give users a tool to explore where LMs may have learned to generate certain word sequences, focusing on verbatim matching as the most direct connection between LM outputs and the training data.”* - from [2]

**Tracing strategy.** The key idea behind OLMoTrace is to find examples of long and unique token sequences that are present both in the model’s output and its training dataset. Given a prompt and LLM response as input, OLMoTrace will return the following:

A set of notable textual spans found in the LLM’s response.

A list of the most relevant document spans from the LLM’s training data associated with each response span. 

Unlike vector search, these matches between the model’s output and training data must be verbatim. Exact token matches can be quickly identified with a suffix array, as discussed in the last section. However, ensuring that the best possible matching documents are identified and returned requires a four-step algorithm that is built on top of the standard infini-gram functionality.

**(Step 1) Maximal Matching Spans. **After tokenizing the LLM’s response, we find all text spans in this response that satisfy three properties:

*Existence*: the span has an exact match in the training data. 

*Maximality*: the span is not a sub-span of another matching span. 

*Self-contained*: the span is not incomplete; e.g., beginning or ending with incomplete words or containing punctuation in the middle of the span. 

These properties are illustrated within the figure below. Here, we see that there are three matching spans. However, all spans except for one—*outlined in green*—are removed due to either not being *i)* maximal or *ii)* self-contained.

![](https://substackcdn.com/image/fetch/$s_!xZn3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57e984b7-bba7-44d3-a877-c3d74693180d_2178x642.png)

Illustration of maximal and self-contained spans

Computing maximal spans naively is inefficient, but authors in [2] propose a more efficient algorithm that relies upon the `find` operation in the infini-gram index. Given a sequence of tokens as input, the `find` operation returns:

The count of matching spans in the index.

A range of segments[8](#footnote-8) that can be used to look up matching data spans. 

However, if the returned count is zero—*indicating that our data has no exact matches for this sequence*—the `find` operation will still return an (empty) segment range. Because the suffix array is sorted lexicographically, the index of this range corresponds to the longest matching prefix of the sequence in our dataset.

# run find operation with infini-gram engine
result = engine.find(input_ids=inp_ids)

"""
### .find() output example (match): 
    {
        'cnt': 10,
        'segment_by_shard': [(13693395, 13693405)],
    }

### .find() output example (no match):
    {
        'cnt': 0,
        'segment_by_shard': [(85267640, 85267640)],
    }
"""

# lookup training documents from .find()
rank_start, rank_end = result['segment_by_shard'][0]
ranks = [r for r in range(rank_start, rank_end)]
for r in ranks:
    docs = engine.get_doc_by_rank(
        s=0,  # assumes suffix array has a single shard
        rank=r,
        max_disp_len=len(inp_ids) * 5,  # size of doc chunk
    )
    doc_text = [tokenizer.decode(d['token_ids']) for d in docs]
    print(f'Number of documents: {len(docs)}')
    print(f'Matching document: {doc_text[0]}')

This property of the `find` operation is leveraged in [2] to create an efficient algorithm for span matching. As shown in the figure below, this algorithm operates by running a single `find` operation for every suffix of the input sequence, *yielding the longest matching prefix for each suffix*. Once all of these matching spans have been identified, we can make another pass through this list to remove any matching spans that are not maximal or self-contained. 

![](https://substackcdn.com/image/fetch/$s_!ofmw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb435fcab-0df9-4a07-b6f4-fc7c07e646d7_2314x804.png)

(from [2])

**(Step 2) Span Filtering.** If our list of maximal spans computed as described above is long, we need some strategy to identify the most useful and relevant of these spans. To do this, authors in [2] score spans according to their span unigram probability (lower is better)—*or the product of unigram probabilities for each token in the span.* The unigram probability of a given token, which is usually precomputed for all tokens and stored in a cache, can be computed as shown below.

![](https://substackcdn.com/image/fetch/$s_!QtrX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb6f7bb6-632c-40d1-bfbf-db4f585a4969_1090x466.png)

Computing a token’s unigram probability

In [2], authors sort spans by their span unigram probability and keep only the first `K` spans in this list, where `K = ceil(0.05 x L)` for a sequence of length `L`.

**(Step 3-4) Merge Spans and Get Documents.** To avoid clutter, overlapping spans are merged together in OLMoTrace. Documents for each of these final spans are retrieved. But, the number of documents associated with each span can be large, so we must sub-select documents; e.g., authors in [2] retain ten documents per span. To find the most relevant documents, we can rank them according to the [BM25 score](https://pypi.org/project/rank-bm25/) between the LLM’s output and the retrieved document.

*“To prioritize showing the most relevant documents, in the document panel we rank all documents by a BM25 score in descending order. The per-document BM25 score is computed by treating the collection of retrieved documents as a corpus, and the concatenation of user prompt and LM response as the query.”* - from [2]

![](https://substackcdn.com/image/fetch/$s_!rZWx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F250f798c-fb39-46d7-83c4-da76cbbeccda_2150x1062.png)

(from [2])

**Example implementation.** The inference pipeline for OLMoTrace is shown in the figure above. To better understand how this works, let’s (quickly) implement the core functionality using the infini-gram package in Python. To build an infini-gram index, we need to put all of our LLM’s training data into a single directory. The infini-gram package expects the data to be formatted as one or more `.jsonl` files, where each file contains `text` and `metadata` fields; see below. Each line of the `.jsonl` file corresponds to a single document in our training dataset.

{
    'text': 'This is a training sequence for our LLM...',
    'metadata': {
        'source': <url>,
        'category': 'general',
        'year': 2025,
        ...
    },
}

Once our data has been formatted as such, we can build the infini-gram index as outlined before. Additionally, OLMoTrace requires us to pre-compute unigram probabilities for all tokens. Both of these steps are implemented below. This code assumes that we use the [Llama 2 tokenizer](https://huggingface.co/meta-llama/Llama-2-7b-hf) to perform tracing and that we only require a single shard for our infini-gram index. The underlying tokenizer [can be modified](https://infini-gram.readthedocs.io/en/latest/indexing.html), and support for multiple shards in the index may be required when working with very large datasets (i.e., more than 500B tokens).

\n    
\n      
\n        
\n  
\n    \n    
\n\n        \n
\n\n  \n  
\n  \n    

\n\n    \n      This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.\n      Learn more about bidirectional Unicode characters\n    \n\n\n  
            Show hidden characters\n\n
\n
\n\n  \n    \n    

\n\n\n\n  \n        
\n          \n          import os\n        
\n        
\n          \n          import json\n        
\n        
\n          \n          from collections import Counter\n        
\n        
\n          \n          import tempfile\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          from transformers import AutoTokenizer\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # load tokenizer / data\n        
\n        
\n          \n          enc = AutoTokenizer.from_pretrained(&quot;meta-llama/Llama-2-7b-hf&quot;, add_bos_token=False, add_eos_token=False)\n        
\n        
\n          \n          data_rows = [{&#39;text&#39;: &#39;here is some training data&#39;}, ...]\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # compute / save unigram probabilities\n        
\n        
\n          \n          all_toks = []\n        
\n        
\n          \n          for x in data_rows:\n        
\n        
\n          \n              all_toks.extend(enc.encode(x[&#39;text&#39;]))\n        
\n        
\n          \n          total_toks = len(all_toks)\n        
\n        
\n          \n          tok_count = Counter(all_toks)\n        
\n        
\n          \n          unigram_probs = {}\n        
\n        
\n          \n          for tid in tok_count:\n        
\n        
\n          \n              cnt = tok_count[tid]\n        
\n        
\n          \n              unigram_probs[tid] = cnt / total_toks\n        
\n        
\n          \n          with open(&lt;save path&gt;, &#39;w&#39;) as json_file:\n        
\n        
\n          \n              json.dump(unigram_probs, json_file, indent=4)\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # build infinigram index\n        
\n        
\n          \n          data_dir = &lt;path to data&gt;\n        
\n        
\n          \n          save_dir = &lt;save index here&gt;\n        
\n        
\n          \n          temp_dir = tempfile.TemporaryDirectory()\n        
\n        
\n          \n          command = (\n        
\n        
\n          \n              f&quot;python -m infini_gram.indexing --data_dir {data_dir} &quot;\n        
\n        
\n          \n              f&quot;--temp_dir {temp_dir.name} --save_dir {save_dir} &quot;\n        
\n        
\n          \n              f&quot;--tokenizer llama --cpus 12 --mem 64  --shards 1 &quot;\n        
\n        
\n          \n              f&quot;--add_metadata --ulimit 100000 &quot;\n        
\n        
\n          \n          )\n        
\n        
\n          \n          print(command)\n        
\n        
\n          \n          os.system(command)\n        
\n        
\n          \n          temp_dir.cleanup()\n        
\n  \n
\n\n\n    
\n\n  
\n
\n\n      
\n      
\n        view raw\n        \n          olmo_trace_index.py\n        \n        hosted with &#10084; by GitHub\n      
\n    
\n
\n","stylesheet":"https://github.githubassets.com/assets/gist-embed-b1ee75c43dbe.css"}" data-component-name="GitgistToDOM">

    

      

        

  

    
    

        

  
  

  
    

    
      This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
      [Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)
    

  
            Show hidden characters

  
    
    

  
        

          
          import os
        

        

          
          import json
        

        

          
          from collections import Counter
        

        

          
          import tempfile
        

        

          
          

        

        

          
          from transformers import AutoTokenizer
        

        

          
          

        

        

          
          # load tokenizer / data
        

        

          
          enc = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", add_bos_token=False, add_eos_token=False)
        

        

          
          data_rows = [{'text': 'here is some training data'}, ...]
        

        

          
          

        

        

          
          # compute / save unigram probabilities
        

        

          
          all_toks = []
        

        

          
          for x in data_rows:
        

        

          
              all_toks.extend(enc.encode(x['text']))
        

        

          
          total_toks = len(all_toks)
        

        

          
          tok_count = Counter(all_toks)
        

        

          
          unigram_probs = {}
        

        

          
          for tid in tok_count:
        

        

          
              cnt = tok_count[tid]
        

        

          
              unigram_probs[tid] = cnt / total_toks
        

        

          
          with open(<save path>, 'w') as json_file:
        

        

          
              json.dump(unigram_probs, json_file, indent=4)
        

        

          
          

        

        

          
          # build infinigram index
        

        

          
          data_dir = <path to data>
        

        

          
          save_dir = <save index here>
        

        

          
          temp_dir = tempfile.TemporaryDirectory()
        

        

          
          command = (
        

        

          
              f"python -m infini_gram.indexing --data_dir {data_dir} "
        

        

          
              f"--temp_dir {temp_dir.name} --save_dir {save_dir} "
        

        

          
              f"--tokenizer llama --cpus 12 --mem 64  --shards 1 "
        

        

          
              f"--add_metadata --ulimit 100000 "
        

        

          
          )
        

        

          
          print(command)
        

        

          
          os.system(command)
        

        

          
          temp_dir.cleanup()
        

  

    

  

      

      

        [view raw](https://gist.github.com/wolfecameron/6120678a88bf52d7be524266c82c409a/raw/b3f5df3886bcbad62089db0f476ba02e6bdaa7c0/olmo_trace_index.py)
        
          olmo_trace_index.py
        
        hosted with ❤ by [GitHub](https://github.com)
      

    

Now that the infini-gram index has been built, we can trace a sequence of text over our training dataset—*following the algorithm proposed by OLMoTrace in [2]*—as shown in the code below. This code returns both a set of spans and their associated documents with metadata from the training corpus.

\n    
\n      
\n        
\n  
\n    \n    
\n\n        \n
\n\n  \n  
\n  \n    

\n\n    \n      This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.\n      Learn more about bidirectional Unicode characters\n    \n\n\n  
            Show hidden characters\n\n
\n
\n\n  \n    \n    

\n\n\n\n  \n        
\n          \n          import ast\n        
\n        
\n          \n          import math\n        
\n        
\n          \n          import random\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          from infini_gram.engine import InfiniGramEngine\n        
\n        
\n          \n          from transformers import AutoTokenizer\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          def compute_longest_prefix(query, doc):\n        
\n        
\n          \n              &quot;&quot;&quot;helper function for computing longest prefix of query that exists\n        
\n        
\n          \n              within a document&quot;&quot;&quot;\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              def shared_prefix_length(list1, list2):\n        
\n        
\n          \n                  prefix_length = 0    \n        
\n        
\n          \n                  for elem1, elem2 in zip(list1, list2):\n        
\n        
\n          \n                      if elem1 == elem2:\n        
\n        
\n          \n                          prefix_length += 1\n        
\n        
\n          \n                      else:\n        
\n        
\n          \n                          break\n        
\n        
\n          \n                  return prefix_length\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              first_id = query[0]\n        
\n        
\n          \n              start_idx = [index for index, value in enumerate(doc) if value == first_id]\n        
\n        
\n          \n              longest_prefix = 0\n        
\n        
\n          \n              for si in start_idx:\n        
\n        
\n          \n                  longest_prefix = max(\n        
\n        
\n          \n                      longest_prefix,\n        
\n        
\n          \n                      shared_prefix_length(query, doc[si:]),\n        
\n        
\n          \n                  )\n        
\n        
\n          \n              return longest_prefix\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # setup\n        
\n        
\n          \n          enc = AutoTokenizer.from_pretrained(&quot;meta-llama/Llama-2-7b-hf&quot;, add_bos_token=False, add_eos_token=False)\n        
\n        
\n          \n          engine = InfiniGramEngine(index_dir=&lt;path to index&gt;, eos_token_id=enc.eos_token_id)\n        
\n        
\n          \n          unigram_probs = {1: 0.5, 2: 0.5} # load pre-computed probabilities\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # LLM output / query to search\n        
\n        
\n          \n          generation = &#39;Here is the output of the LLM that we want to search for in our data.&#39;\n        
\n        
\n          \n          gen_ids = enc.encode(generation)\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          Step One: find maximal matching spans\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          L = len(gen_ids)\n        
\n        
\n          \n          max_doc_toks = len(gen_ids) * 2  # size of spans to retrieve in documents\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # find longest prefix match for every suffix in the query\n        
\n        
\n          \n          spans = []\n        
\n        
\n          \n          for start in range(len(gen_ids) - 1):\n        
\n        
\n          \n              _suffix = gen_ids[start:]\n        
\n        
\n          \n              _suff_res = engine.find(input_ids=_suffix)\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              # if no match, get the longest matching prefix using find result\n        
\n        
\n          \n              if _suff_res[&#39;cnt&#39;] == 0:\n        
\n        
\n          \n                  _shards = _suff_res[&#39;segment_by_shard&#39;]\n        
\n        
\n          \n                  assert len(_shards) == 1  # assume only one shard\n        
\n        
\n          \n                  _doc_ids = engine.get_doc_by_rank(\n        
\n        
\n          \n                      s=0,  # assume only one shard\n        
\n        
\n          \n                      rank=_shards[0][0],\n        
\n        
\n          \n                      max_disp_len=max_doc_toks,\n        
\n        
\n          \n                  )[&#39;token_ids&#39;]\n        
\n        
\n          \n                  matched_toks = compute_longest_prefix(_suffix, _doc_ids)  # get longest matching prefix\n        
\n        
\n          \n              elif _suff_res[&#39;cnt&#39;] &gt; 0:\n        
\n        
\n          \n                  matched_toks = len(_suffix)\n        
\n        
\n          \n              spans.append((start, start + matched_toks))\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # remove partial and non-self-contained spans\n        
\n        
\n          \n          full_spans = []\n        
\n        
\n          \n          for start, end in spans:\n        
\n        
\n          \n              span_ids = gen_ids[start: end]\n        
\n        
\n          \n              span_text = enc.decode(span_ids)\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              # check for internal punctuation\n        
\n        
\n          \n              has_internal_punc = False\n        
\n        
\n          \n              punc_chars = &quot;!.?\\n&quot;\n        
\n        
\n          \n              for ch in span_text[:-1]:\n        
\n        
\n          \n                  if ch in punc_chars:\n        
\n        
\n          \n                      has_internal_punc = True\n        
\n        
\n          \n                      break\n        
\n        
\n          \n              if has_internal_punc:\n        
\n        
\n          \n                  continue\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              # check if first token is a continuation of a word\n        
\n        
\n          \n              first_tok_id = span_ids[0]\n        
\n        
\n          \n              first_tok = enc.convert_ids_to_tokens(first_tok_id)\n        
\n        
\n          \n              if first_tok[0] != &#39;▁&#39;:  # assumes Llama 2 token format\n        
\n        
\n          \n                  continue\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              # no sub-token follows the last token\n        
\n        
\n          \n              if end &lt; len(gen_ids) and tokenizer.convert_ids_to_tokens(gen_ids[end])[0] != &quot;▁&quot;:\n        
\n        
\n          \n                  continue\n        
\n        
\n          \n              full_spans.append((start, end, span_ids, span_text))    \n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # remove non-maximal spans\n        
\n        
\n          \n          maximal_spans = []\n        
\n        
\n          \n          max_end_pos = -1\n        
\n        
\n          \n          full_spans = sorted(full_spans)\n        
\n        
\n          \n          for start, end, ids, text in full_spans:\n        
\n        
\n          \n              if end &gt; max_end_pos:\n        
\n        
\n          \n                  maximal_spans.append((start, end, ids, text))\n        
\n        
\n          \n                  max_end_pos = end\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          Step Two: filter to keep long / unique spans\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          K = math.ceil(0.05 * L)\n        
\n        
\n          \n          assert K &gt; 0\n        
\n        
\n          \n          filt_spans = []\n        
\n        
\n          \n          for start, end, ids, text in maximal_spans:\n        
\n        
\n          \n              span_uni_prob = [unigram_probs.get(_id) for _id in ids]\n        
\n        
\n          \n              span_uni_prob = math.prod(span_uni_prob)\n        
\n        
\n          \n              filt_spans.append((start, end, ids, text, span_uni_prob))\n        
\n        
\n          \n          filt_spans = sorted(filt_spans, key=lambda x: x[-1])\n        
\n        
\n          \n          filt_spans = filt_spans[:K]\n        
\n        
\n          \n          filt_spans = sorted(filt_spans)  # sort based on start position again\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          Step Three: retrieve Enclosing Docs\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          docs_per_span = 10\n        
\n        
\n          \n          span_to_docs = defaultdict(list)\n        
\n        
\n          \n          for i, (start, end, ids, text, uni_prob) in enumerate(filt_spans):\n        
\n        
\n          \n              # run retrieval in infinigram index to get documents\n        
\n        
\n          \n              span_res = engine.find(input_ids=ids)\n        
\n        
\n          \n              assert span_res[&#39;cnt&#39;] &gt; 0\n        
\n        
\n          \n              assert len(span_res[&#39;segment_by_shard&#39;]) == 1  # assume only one shard\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              rank_start, rank_end = span_res[&#39;segment_by_shard&#39;][0]\n        
\n        
\n          \n              ranks = [r for r in range(rank_start, rank_end)]\n        
\n        
\n          \n              if len(ranks) &gt; docs_per_span:\n        
\n        
\n          \n                  # retrieve fixed number of documents for each span\n        
\n        
\n          \n                  ranks = sorted(random.sample(ranks, docs_per_span))\n        
\n        
\n          \n          \n\n        
\n        
\n          \n              # NOTE: we can instead rank documents by BM25 score here!\n        
\n        
\n          \n              for r in ranks:\n        
\n        
\n          \n                  _doc = engine.get_doc_by_rank(\n        
\n        
\n          \n                      s=0,\n        
\n        
\n          \n                      rank=r,\n        
\n        
\n          \n                      max_disp_len=max_doc_toks,\n        
\n        
\n          \n                  )\n        
\n        
\n          \n                  _doc_meta = ast.literal_eval(_doc[&#39;metadata&#39;])[&#39;metadata&#39;]\n        
\n        
\n          \n                  _doc_text = enc.decode(_doc[&#39;token_ids&#39;])\n        
\n        
\n          \n                  _doc_data = {\n        
\n        
\n          \n                      &quot;text&quot;: _doc_text,\n        
\n        
\n          \n                      **_doc_meta\n        
\n        
\n          \n                  }\n        
\n        
\n          \n                  span_to_docs[i].append(_doc_data)\n        
\n        
\n          \n          \n\n        
\n        
\n          \n                  \n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          Step Four: merge overlapping spans\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          # get indices of spans to merge together\n        
\n        
\n          \n          merged_spans = [[0]]\n        
\n        
\n          \n          curr_idx = 0\n        
\n        
\n          \n          curr_start = filt_spans[0][0]\n        
\n        
\n          \n          curr_end = filt_spans[0][1]\n        
\n        
\n          \n          for i, next_span in enumerate(filt_spans[1:]):\n        
\n        
\n          \n              start = next_span[0]\n        
\n        
\n          \n              end = next_span[1]\n        
\n        
\n          \n              if start &lt; curr_end:\n        
\n        
\n          \n                  curr_end = max(curr_end, end)\n        
\n        
\n          \n                  merged_spans[curr_idx].append(i + 1)\n        
\n        
\n          \n              else:\n        
\n        
\n          \n                  curr_start, curr_end = start, end\n        
\n        
\n          \n                  curr_idx += 1\n        
\n        
\n          \n                  merged_spans.append([i + 1])\n        
\n        
\n          \n                  assert len(merged_spans) == curr_idx + 1\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          # merge spans into a final set\n        
\n        
\n          \n          final_spans = []\n        
\n        
\n          \n          for ms in merged_spans:\n        
\n        
\n          \n              all_docs = []\n        
\n        
\n          \n              docs_per_merged_span = math.ceil(docs_per_span / float(len(ms)))  # subsample docs for spans being merged\n        
\n        
\n          \n              for i in ms:\n        
\n        
\n          \n                  # take top docs from each span being merged\n        
\n        
\n          \n                  all_docs.extend(span_to_docs[i][:docs_per_merged_span])\n        
\n        
\n          \n              _spans = [filt_spans[i] for i in ms]\n        
\n        
\n          \n              start = min([x[0] for x in _spans])\n        
\n        
\n          \n              end = max([x[1] for x in _spans])\n        
\n        
\n          \n              text = enc.decode(gen_ids[start: end])\n        
\n        
\n          \n              final_spans.append({\n        
\n        
\n          \n                  &quot;start&quot;: start,\n        
\n        
\n          \n                  &quot;end&quot;: end,\n        
\n        
\n          \n                  &quot;text&quot;: text,\n        
\n        
\n          \n                  &quot;docs&quot;: all_docs,\n        
\n        
\n          \n              })\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          \n\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          Step Five: observe tracing results\n        
\n        
\n          \n          &quot;&quot;&quot;\n        
\n        
\n          \n          docs_to_print = 5\n        
\n        
\n          \n          print(f&#39;Query Text: {enc.decode(gen_ids)}&#39;)\n        
\n        
\n          \n          for i, sp in enumerate(final_spans):\n        
\n        
\n          \n              print(&quot;\\n&quot; + &quot;=&quot;*20 + f&quot; SPAN {i + 1} / {len(final_spans)} &quot; + &quot;=&quot;*20)\n        
\n        
\n          \n              print(f&quot;Span Text: {sp[&#39;text&#39;]}\\n&quot;)\n        
\n        
\n          \n              for j, doc in enumerate(sp[&#39;docs&#39;]):\n        
\n        
\n          \n                  print(&quot;-&quot;*10 + f&quot; Document {j + 1} / {len(sp[&#39;docs&#39;])} &quot; + &quot;-&quot;*10)\n        
\n        
\n          \n                  for k in [&#39;text&#39;, &#39;movie_id&#39;, &#39;src_lang&#39;, &#39;start_frame&#39;, &#39;end_frame&#39;]:\n        
\n        
\n          \n                      if k == &#39;text&#39;:\n        
\n        
\n          \n                          v = doc[k].replace(&#39;\\n&#39;, &#39; &#39;)\n        
\n        
\n          \n                      else:\n        
\n        
\n          \n                          v = doc[k]\n        
\n        
\n          \n                      print(f&quot;- {k} --&gt; {v}&quot;)\n        
\n  \n
\n\n\n    
\n\n  
\n
\n\n      
\n      
\n        view raw\n        \n          olmo_trace.py\n        \n        hosted with &#10084; by GitHub\n      
\n    
\n
\n","stylesheet":"https://github.githubassets.com/assets/gist-embed-b1ee75c43dbe.css"}" data-component-name="GitgistToDOM">

    

      

        

  

    
    

        

  
  

  
    

    
      This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
      [Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)
    

  
            Show hidden characters

  
    
    

  
        

          
          import ast
        

        

          
          import math
        

        

          
          import random
        

        

          
          

        

        

          
          from infini_gram.engine import InfiniGramEngine
        

        

          
          from transformers import AutoTokenizer
        

        

          
          

        

        

          
          def compute_longest_prefix(query, doc):
        

        

          
              """helper function for computing longest prefix of query that exists
        

        

          
              within a document"""
        

        

          
          

        

        

          
              def shared_prefix_length(list1, list2):
        

        

          
                  prefix_length = 0    
        

        

          
                  for elem1, elem2 in zip(list1, list2):
        

        

          
                      if elem1 == elem2:
        

        

          
                          prefix_length += 1
        

        

          
                      else:
        

        

          
                          break
        

        

          
                  return prefix_length
        

        

          
          

        

        

          
              first_id = query[0]
        

        

          
              start_idx = [index for index, value in enumerate(doc) if value == first_id]
        

        

          
              longest_prefix = 0
        

        

          
              for si in start_idx:
        

        

          
                  longest_prefix = max(
        

        

          
                      longest_prefix,
        

        

          
                      shared_prefix_length(query, doc[si:]),
        

        

          
                  )
        

        

          
              return longest_prefix
        

        

          
          

        

        

          
          # setup
        

        

          
          enc = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", add_bos_token=False, add_eos_token=False)
        

        

          
          engine = InfiniGramEngine(index_dir=<path to index>, eos_token_id=enc.eos_token_id)
        

        

          
          unigram_probs = {1: 0.5, 2: 0.5} # load pre-computed probabilities
        

        

          
          

        

        

          
          # LLM output / query to search
        

        

          
          generation = 'Here is the output of the LLM that we want to search for in our data.'
        

        

          
          gen_ids = enc.encode(generation)
        

        

          
          

        

        

          
          

        

        

          
          """
        

        

          
          Step One: find maximal matching spans
        

        

          
          """
        

        

          
          L = len(gen_ids)
        

        

          
          max_doc_toks = len(gen_ids) * 2  # size of spans to retrieve in documents
        

        

          
          

        

        

          
          # find longest prefix match for every suffix in the query
        

        

          
          spans = []
        

        

          
          for start in range(len(gen_ids) - 1):
        

        

          
              _suffix = gen_ids[start:]
        

        

          
              _suff_res = engine.find(input_ids=_suffix)
        

        

          
          

        

        

          
              # if no match, get the longest matching prefix using find result
        

        

          
              if _suff_res['cnt'] == 0:
        

        

          
                  _shards = _suff_res['segment_by_shard']
        

        

          
                  assert len(_shards) == 1  # assume only one shard
        

        

          
                  _doc_ids = engine.get_doc_by_rank(
        

        

          
                      s=0,  # assume only one shard
        

        

          
                      rank=_shards[0][0],
        

        

          
                      max_disp_len=max_doc_toks,
        

        

          
                  )['token_ids']
        

        

          
                  matched_toks = compute_longest_prefix(_suffix, _doc_ids)  # get longest matching prefix
        

        

          
              elif _suff_res['cnt'] > 0:
        

        

          
                  matched_toks = len(_suffix)
        

        

          
              spans.append((start, start + matched_toks))
        

        

          
          

        

        

          
          # remove partial and non-self-contained spans
        

        

          
          full_spans = []
        

        

          
          for start, end in spans:
        

        

          
              span_ids = gen_ids[start: end]
        

        

          
              span_text = enc.decode(span_ids)
        

        

          
          

        

        

          
              # check for internal punctuation
        

        

          
              has_internal_punc = False
        

        

          
              punc_chars = "!.?\n"
        

        

          
              for ch in span_text[:-1]:
        

        

          
                  if ch in punc_chars:
        

        

          
                      has_internal_punc = True
        

        

          
                      break
        

        

          
              if has_internal_punc:
        

        

          
                  continue
        

        

          
          

        

        

          
              # check if first token is a continuation of a word
        

        

          
              first_tok_id = span_ids[0]
        

        

          
              first_tok = enc.convert_ids_to_tokens(first_tok_id)
        

        

          
              if first_tok[0] != '▁':  # assumes Llama 2 token format
        

        

          
                  continue
        

        

          
          

        

        

          
              # no sub-token follows the last token
        

        

          
              if end < len(gen_ids) and tokenizer.convert_ids_to_tokens(gen_ids[end])[0] != "▁":
        

        

          
                  continue
        

        

          
              full_spans.append((start, end, span_ids, span_text))    
        

        

          
          

        

        

          
          # remove non-maximal spans
        

        

          
          maximal_spans = []
        

        

          
          max_end_pos = -1
        

        

          
          full_spans = sorted(full_spans)
        

        

          
          for start, end, ids, text in full_spans:
        

        

          
              if end > max_end_pos:
        

        

          
                  maximal_spans.append((start, end, ids, text))
        

        

          
                  max_end_pos = end
        

        

          
          

        

        

          
          

        

        

          
          """
        

        

          
          Step Two: filter to keep long / unique spans
        

        

          
          """
        

        

          
          K = math.ceil(0.05 * L)
        

        

          
          assert K > 0
        

        

          
          filt_spans = []
        

        

          
          for start, end, ids, text in maximal_spans:
        

        

          
              span_uni_prob = [unigram_probs.get(_id) for _id in ids]
        

        

          
              span_uni_prob = math.prod(span_uni_prob)
        

        

          
              filt_spans.append((start, end, ids, text, span_uni_prob))
        

        

          
          filt_spans = sorted(filt_spans, key=lambda x: x[-1])
        

        

          
          filt_spans = filt_spans[:K]
        

        

          
          filt_spans = sorted(filt_spans)  # sort based on start position again
        

        

          
          

        

        

          
          

        

        

          
          """
        

        

          
          Step Three: retrieve Enclosing Docs
        

        

          
          """
        

        

          
          docs_per_span = 10
        

        

          
          span_to_docs = defaultdict(list)
        

        

          
          for i, (start, end, ids, text, uni_prob) in enumerate(filt_spans):
        

        

          
              # run retrieval in infinigram index to get documents
        

        

          
              span_res = engine.find(input_ids=ids)
        

        

          
              assert span_res['cnt'] > 0
        

        

          
              assert len(span_res['segment_by_shard']) == 1  # assume only one shard
        

        

          
          

        

        

          
              rank_start, rank_end = span_res['segment_by_shard'][0]
        

        

          
              ranks = [r for r in range(rank_start, rank_end)]
        

        

          
              if len(ranks) > docs_per_span:
        

        

          
                  # retrieve fixed number of documents for each span
        

        

          
                  ranks = sorted(random.sample(ranks, docs_per_span))
        

        

          
          

        

        

          
              # NOTE: we can instead rank documents by BM25 score here!
        

        

          
              for r in ranks:
        

        

          
                  _doc = engine.get_doc_by_rank(
        

        

          
                      s=0,
        

        

          
                      rank=r,
        

        

          
                      max_disp_len=max_doc_toks,
        

        

          
                  )
        

        

          
                  _doc_meta = ast.literal_eval(_doc['metadata'])['metadata']
        

        

          
                  _doc_text = enc.decode(_doc['token_ids'])
        

        

          
                  _doc_data = {
        

        

          
                      "text": _doc_text,
        

        

          
                      **_doc_meta
        

        

          
                  }
        

        

          
                  span_to_docs[i].append(_doc_data)
        

        

          
          

        

        

          
                  
        

        

          
          """
        

        

          
          Step Four: merge overlapping spans
        

        

          
          """
        

        

          
          # get indices of spans to merge together
        

        

          
          merged_spans = [[0]]
        

        

          
          curr_idx = 0
        

        

          
          curr_start = filt_spans[0][0]
        

        

          
          curr_end = filt_spans[0][1]
        

        

          
          for i, next_span in enumerate(filt_spans[1:]):
        

        

          
              start = next_span[0]
        

        

          
              end = next_span[1]
        

        

          
              if start < curr_end:
        

        

          
                  curr_end = max(curr_end, end)
        

        

          
                  merged_spans[curr_idx].append(i + 1)
        

        

          
              else:
        

        

          
                  curr_start, curr_end = start, end
        

        

          
                  curr_idx += 1
        

        

          
                  merged_spans.append([i + 1])
        

        

          
                  assert len(merged_spans) == curr_idx + 1
        

        

          
          

        

        

          
          # merge spans into a final set
        

        

          
          final_spans = []
        

        

          
          for ms in merged_spans:
        

        

          
              all_docs = []
        

        

          
              docs_per_merged_span = math.ceil(docs_per_span / float(len(ms)))  # subsample docs for spans being merged
        

        

          
              for i in ms:
        

        

          
                  # take top docs from each span being merged
        

        

          
                  all_docs.extend(span_to_docs[i][:docs_per_merged_span])
        

        

          
              _spans = [filt_spans[i] for i in ms]
        

        

          
              start = min([x[0] for x in _spans])
        

        

          
              end = max([x[1] for x in _spans])
        

        

          
              text = enc.decode(gen_ids[start: end])
        

        

          
              final_spans.append({
        

        

          
                  "start": start,
        

        

          
                  "end": end,
        

        

          
                  "text": text,
        

        

          
                  "docs": all_docs,
        

        

          
              })
        

        

          
          

        

        

          
          

        

        

          
          """
        

        

          
          Step Five: observe tracing results
        

        

          
          """
        

        

          
          docs_to_print = 5
        

        

          
          print(f'Query Text: {enc.decode(gen_ids)}')
        

        

          
          for i, sp in enumerate(final_spans):
        

        

          
              print("\n" + "="*20 + f" SPAN {i + 1} / {len(final_spans)} " + "="*20)
        

        

          
              print(f"Span Text: {sp['text']}\n")
        

        

          
              for j, doc in enumerate(sp['docs']):
        

        

          
                  print("-"*10 + f" Document {j + 1} / {len(sp['docs'])} " + "-"*10)
        

        

          
                  for k in ['text', 'movie_id', 'src_lang', 'start_frame', 'end_frame']:
        

        

          
                      if k == 'text':
        

        

          
                          v = doc[k].replace('\n', ' ')
        

        

          
                      else:
        

        

          
                          v = doc[k]
        

        

          
                      print(f"- {k} --> {v}")
        

  

    

  

      

      

        [view raw](https://gist.github.com/wolfecameron/306aa72a0c5095db460e2ccea9b06777/raw/e1040a0e8198f9d82bbe20bcc7246416ed80bb0f/olmo_trace.py)
        
          olmo_trace.py
        
        hosted with ❤ by [GitHub](https://github.com)
      

    

As we can see, the core functionality of OLMoTrace is not that complicated—*most of the complex code is already abstracted away by the infini-gram package*! For those who are interested, I would highly recommend testing out this code on your own model and data to get a feel for the types of results it can return!

![](https://substackcdn.com/image/fetch/$s_!pLsI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F332e82aa-8b1d-4c48-8baf-13d820ba8e81_1840x432.png)

OLMoTrace use cases (from [2])

**Applications of OLMoTrace. **OLMoTrace specializes in finding long and unique spans that exactly match between an LLM’s output and its training data. Exact matches are a useful proxy for finding training data that may contribute to a certain output from our LLM. In [2], a variety of different use cases are considered:

*Fact checking*: compare factual statements made by the LLM to similar factual statements within its training data. 

*Creative expressions*: check if “creative” outputs from the LLM are actually creative, or just directly copied from training data. 

*Reasoning capabilities*: check if the LLM copies the reasoning process used to solve verifiable problems (e.g., math) from its training data. 

In each of these cases, we can learn something new about our LLM by tracing its output to find regions of the training data with a notable, verbatim match.

Reasoning Models and Future Research

![](https://substackcdn.com/image/fetch/$s_!Brs9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3ea8fb-4672-4580-b9e5-6f9520114cf0_2344x498.png)

Stages of LLM training (from [4, 5, 6])

**Extension to reasoning models.** As shown above, LLMs are usually trained in several phases, each of which have unique styles of data:

*[Supervised Finetuning (SFT)](https://cameronrwolfe.substack.com/p/understanding-and-using-supervised)*: trains the LLM using concrete examples of prompt-response pairs that the LLM should replicate.

*[Reinforcement Learning from Human Feedback (RLHF)](https://cameronrwolfe.substack.com/p/the-story-of-rlhf-origins-motivations)*: trains the model using preference pairs (i.e., a single prompt with two responses, where one of the two responses is identified as better than the other). 

*[Reinforcement Learning from Verifiable Rewards (RLVR)](https://cameronrwolfe.substack.com/p/demystifying-reasoning-models)*: uses pure RL to reward the model for correctly solving verifiable problems as determined by a rule-based (usually deterministic) verification function. 

Despite these unique data formats, we can apply OLMoTrace to each stage of training with minimal changes! We can easily build an infini-gram index over supervised examples and preference pairs (though we may want to treat the positive and negative completions in the preference pair differently). For RLVR, however, *we may need to think more deeply about how the data should be traced*.

![](https://substackcdn.com/image/fetch/$s_!zfsl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb865992-1eee-4fdb-b98a-165f4d555e11_1774x608.png)

When training an LLM with RLVR, we have a dataset of problems with verifiable solutions; e.g., a math problem with a known solution or a coding problem with test cases. We can easily check whether the LLM solves such problems correctly (e.g., by string matching or something slightly more robust); see above. Then, the model learns how to solve these problems on its own via a self-evolution process powered by large-scale RL training, as demonstrated by [DeepSeek-R1](https://cameronrwolfe.substack.com/i/153722335/open-reasoning-deepseek-r-and-more) [7].

*“We explore the potential of LLMs to develop reasoning capabilities without any supervised data, focusing on their self-evolution through a pure reinforcement learning process.” *- from [7]

During RL training, we see in [7] that LLMs learn to output complex chains of thought—*sometimes* *thousands of tokens in length!*—to improve their reasoning capabilities. If we want to index these reasoning traces, however, we run into an interesting problem. Namely, the reasoning traces are not actually part of our training data—*they are generated by the LLM during the RL training process*.

![](https://substackcdn.com/image/fetch/$s_!COPD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36e006bb-5959-485b-bb4a-d45b235a8a9d_1800x1004.png)

(from [7])

Similarly, the LLM generates completions that are ranked by a reward model and used for policy updates during RLHF; see [here](https://huggingface.co/blog/rlhf) for further explanation. If we want to capture patterns learned during RL training—*including both RLHF and RLVR*—we have to keep track of the completions generated by our LLM during training. Given access to these completions, we can index them like any other training data, add them to an infini-gram index, and trace them using OLMoTrace. 

**Related (and future) research.** Despite the utility of OLMoTrace, exact matches do NOT guarantee causality—*there are many reasons an LLM may have generated an output*. Just because we find training data that is similar to an output from our LLM does not mean that this data is guaranteed to have caused this output. 

Attempting to provide deeper insight into the outputs of an LLM, several parallel veins of research are investigating alternative strategies for explainability. For example, many papers have been recently published on the topic of teaching LLMs how to cite sources when generating output [8, 9, 10]; see below. 

![](https://substackcdn.com/image/fetch/$s_!Ss5p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff79a885a-b083-4dc6-b86d-33001a12fd90_1278x838.png)

(from [8])

Such an ability to cite sources can be incorporated into the LLM’s standard training process—*e.g., pretraining [8] or RLHF [9]*—such that the model learns when and how to provide evidence for its answers. However, there is still no guarantee that these citations truly explain how an output was generated.

The field of [mechanistic interpretability](https://distill.pub/2020/circuits/zoom-in/) seeks to study the internals of neural networks to gain an understanding of why they produce the outputs that they do. Although deep neural networks are typically portrayed as block boxes, we can discover many repeated circuits and features in these networks when studied at a microscopic level (i.e., small sets of weights). For example, vision networks tend to have dedicated units for detecting curves, edges and much more.

![Abstract Feature Examples](https://substackcdn.com/image/fetch/$s_!EN03!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16d01ddd-a81c-442b-bccd-0f8af4d3c5ca_2200x1660.webp)

The topic of mechanistic interpretability was largely popularized by [Anthropic](https://www.anthropic.com/). In a [recent report](https://www.anthropic.com/research/mapping-mind-language-model), researchers performed a large-scale study of features in Claude Sonnet using [dictionary learning](https://www.anthropic.com/research/towards-monosemanticity-decomposing-language-models-with-dictionary-learning). As shown above, this study discovered millions of features for advanced concepts, such as people, places, bugs in code and more. 

*“We have identified how millions of concepts are represented inside Claude Sonnet, one of our deployed large language models. This is the first ever detailed look inside a modern, production-grade large language model.”* - from [11]

Additionally, authors analyze the “distance” between features and find some interesting properties; e.g., the Golden Gate Bridge feature is close to that of Alcatraz. Such research, though nascent, is arguably the most promising avenue for truly understanding why and how LLMs produce certain outputs.

Conclusions

As we have learned, optimizing our training dataset is one of the most impactful and important aspects of the LLM training process. To effectively curate and debug our data, we should begin by looking at the data itself—*not by training models*! First, we should manually inspect our data and develop an understanding of its various properties, patterns and quirks. To scale the manual inspection process, we can rely upon both heuristics (when possible) and machine learning models; e.g., fastText or LLM judges. This data-focused curation process focuses upon fixing issues and improving data quality before training any LLMs!

*“One pattern I noticed is that great AI researchers are willing to manually inspect lots of data. And more than that, they build infrastructure that allows them to manually inspect data quickly. Though not glamorous, manually examining data gives valuable intuitions about the problem.”* - [Jason Wei](https://x.com/_jasonwei/status/1708921475829481683?s=20)

Once we start training LLMs, we can use the LLM’s outputs to find issues in our data. More specifically, we can:

Identify problematic LLM outputs via our evaluation framework.

Trace these outputs to corresponding regions of the training data.

Although we can use standard search techniques—*like lexical or vector search*—for tracing data, there are specialized tracing techniques that have been specifically developed for LLMs like OLMoTrace [2]. These techniques are easy (and quick) to setup, highly informative and can be scaled to arbitrarily large datasets, *making them a very practical choice for debugging LLM training datasets*.

New to the newsletter?

Hi! I’m [Cameron R. Wolfe](https://cameronrwolfe.me/), Deep Learning Ph.D. and Senior Research Scientist at [Netflix](https://research.netflix.com/research-area/nlp-and-conversations). This is the Deep (Learning) Focus newsletter, where I help readers better understand important topics in AI research. If you like the newsletter, please subscribe, share it, or follow me on [X](https://twitter.com/cwolferesearch) and [LinkedIn](https://www.linkedin.com/in/cameron-r-wolfe-ph-d-04744a238/)!

[Subscribe now](https://cameronrwolfe.substack.com/subscribe?)

Bibliography

[1] Liu, Jiacheng, et al. "Infini-gram: Scaling unbounded n-gram language models to a trillion tokens." *arXiv preprint arXiv:2401.17377* (2024).

[2] Liu, Jiacheng, et al. "OLMoTrace: Tracing Language Model Outputs Back to Trillions of Training Tokens." *arXiv preprint arXiv:2504.07096* (2025).

[3] Touvron, Hugo, et al. "Llama 2: Open foundation and fine-tuned chat models." *arXiv preprint arXiv:2307.09288* (2023).

[4] Kaplan, Jared, et al. "Scaling laws for neural language models." *arXiv preprint arXiv:2001.08361* (2020).

[5] Ouyang, Long, et al. "Training language models to follow instructions with human feedback." *Advances in neural information processing systems* 35 (2022): 27730-27744.

[6] Lambert, Nathan, et al. "T\" ulu 3: Pushing frontiers in open language model post-training." *arXiv preprint arXiv:2411.15124* (2024).

[7] Guo, Daya, et al. "Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning." *arXiv preprint arXiv:2501.12948* (2025).

[8] Khalifa, Muhammad, et al. "Source-aware training enables knowledge attribution in language models." *arXiv preprint arXiv:2404.01019* (2024).

[9] Glaese, Amelia, et al. "Improving alignment of dialogue agents via targeted human judgements, 2022." *URL https://storage. googleapis. com/deepmind-media/DeepMind. com/Authors-Notes/sparrow/sparrow-final. pdf* (2022).

[10] Huang, Chengyu, et al. "Training language models to generate text with citations via fine-grained rewards." *arXiv preprint arXiv:2402.04315* (2024).

[11] Anthropic. “Mapping the Mind of a Large Language Model” [https://www.anthropic.com/research/mapping-mind-language-model](https://www.anthropic.com/research/mapping-mind-language-model) (2025).

[12] Liu, Yang, et al. "G-eval: NLG evaluation using gpt-4 with better human alignment." *arXiv preprint arXiv:2303.16634* (2023).
[13] Meta. “The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation”*[https://ai.meta.com/blog/llama-4-multimodal-intelligence/](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)*(2025).

[1](#footnote-anchor-1)

The papers that generate the largest interest tend to fall into this category; e.g., recent examples include [GRPO](https://arxiv.org/abs/2402.03300), [diffusion LLMs](https://arxiv.org/abs/2502.09992), and [RLVR](https://arxiv.org/abs/2411.15124). 

[2](#footnote-anchor-2)

Specifically, Llama 3 was post-trained using only SFT and DPO, while Llama 4 uses a more sophisticated pipeline of SFT, online RL, and lightweight DPO; see [here](https://cameronrwolfe.substack.com/i/161016210/post-training).

[3](#footnote-anchor-3)

The rule of thumb for what constitutes “enough” manual data inspection is that it’s more than you want it to be. Seriously, spend more time manually inspecting your data. You won’t regret it!

[4](#footnote-anchor-4)

For example, Llama 3 has a multi-stage pretraining process where select data sources (e.g., reasoning datasets) are emphasized more heavily in later stages to improve the model’s capabilities in certain domains; see [here](https://magazine.sebastianraschka.com/i/147749119/pre-training-iii-annealing-on-high-quality-data).

[5](#footnote-anchor-5)

Lexicographical ordering is a generalization of alphabetical ordering to support characters that go beyond the alphabet (e.g., numbers and symbols).

[6](#footnote-anchor-6)

In [1], authors use the `\xff\xff` token as a separator between documents.

[7](#footnote-anchor-7)

Assume that our dataset contains `T` tokens and that the vocabulary size of our tokenizer is ~64K, *meaning that each token ID can be represented with two bytes*. The list of token IDs for this dataset consumes `2T` bytes. The suffix array is a list of `T` indices that point to positions in the token array, where each index is represented with `log(2T)/8` bytes. If `2B < T < 500B`, indices can be stored using 5 bytes, meaning that the combined size of the token and suffix arrays is just `7T` bytes!

[8](#footnote-anchor-8)

These segments are just integers corresponding to the position of a matching span within the full token array.
