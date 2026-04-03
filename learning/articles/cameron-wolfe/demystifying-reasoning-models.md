# Demystifying Reasoning Models

**Source:** https://cameronrwolfe.substack.com/p/demystifying-reasoning-models
**Ingested:** 2026-04-02
**Tags:** llms, rlhf, architectures

---

![](https://substackcdn.com/image/fetch/$s_!pR5Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4fb1867-b78e-4db6-aea7-14251a3facce_2389x1336.png)

(from [4, 13, 22])

For the last several years, we have used a relatively fixed pipeline for training large language models (LLMs); see below. First, we pretrain these language models over raw textual data from the internet. Afterwards, we align them—*or train them to produce outputs that are preferable to humans*—using a combination of [supervised finetuning (SFT)](https://cameronrwolfe.substack.com/p/understanding-and-using-supervised) and [reinforcement learning from human feedback (RLHF)](https://cameronrwolfe.substack.com/p/the-story-of-rlhf-origins-motivations). Both pretraining and alignment play a key role in model quality, but a large majority of advancements in this paradigm have been driven by [LLM scaling laws](https://cameronrwolfe.substack.com/p/llm-scaling-laws)—*we get better results by pretraining larger models on more data*.

![](https://substackcdn.com/image/fetch/$s_!9HTk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac82c7c1-fcbd-4b32-b9cd-febfadd77c19_1720x562.png)

Training pipeline for a standard LLM

Recently, a completely new paradigm in LLM research has emerged: *reasoning*. Reasoning models approach problem solving in a completely different manner compared to standard LLMs. In particular, they spend a variable amount of time “thinking” prior to providing their final answer to a question. Training models that are able to think effectively (e.g., decompose problems, detect errors in their thinking, explore alternative solutions and more) requires new strategies, usually involving large-scale reinforcement learning (RL). Additionally, such models give rise to new forms of scaling laws for training via RL and inference; see below.

![](https://substackcdn.com/image/fetch/$s_!1eNI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88a91669-f7f0-41aa-b0f0-78392da2115a_1254x804.png)

(from [4])

In this overview, we will learn more about recent advancements in reasoning models. To start, we will focus on several (closed) reasoning models that were proposed first by OpenAI. We will contextualize the explanation of these models with the fundamental ideas that underlie LLM reasoning capabilities. Afterwards, we will explore recently-proposed (open) reasoning models, outlining necessary details for creating such a model from scratch. Reasoning models are different from standard LLMs. But, don’t worry. A lot of the key concepts of LLMs still apply to reasoning models. *We will clarify important distinctions throughout.* 

The Age of Reasoning

Just as AI progress was seemingly [starting to slow down](https://cameronrwolfe.substack.com/p/llm-scaling-laws), we witnessed a sudden and significant improvement in LLM capabilities with the popularization of [reasoning models](https://sebastianraschka.com/blog/2025/understanding-reasoning-llms.html). First to be released was OpenAI’s [o1-preview](https://openai.com/index/introducing-openai-o1-preview/) [4], followed by a series of distilled (i.e., smaller) models like o1-mini and later model variants like [o3](https://openai.com/index/openai-o3-mini/) [6]. In response, other companies released similar reasoning models, such as [Google’s Gemini 2.0 Flash Thinking](https://deepmind.google/technologies/gemini/flash-thinking/). In this section, we will explore these initial, closed reasoning models and the basic ideas behind how they work.

Initial Reasoning Models: o1 and o1-mini

*“We've developed a new series of AI models designed to spend more time thinking before they respond.”* - from [4]

The release of **o1-preview** [4, 5] by OpenAI made two things very clear:

Reasoning models can solve verifiable tasks—*such as math and coding tasks*—very accurately.

The approach taken by reasoning models to solve these problems is very different from that of a traditional LLM.

**Long CoT.** The main difference between a reasoning model and a standard LLM is the ability to “think” before answering a question. The reasoning model’s thoughts are just long chains of thought—*or* *long CoT for short, sometimes referred to as a reasoning trace or trajectory*—outputted by the LLM. This long CoT is generated no differently than any other sequence of text. However, these reasoning trajectories exhibit very interesting properties that are more akin to search algorithms than vanilla text generation. For example, the model will:

Think through each part of a complex problem.

Decompose complex problems into smaller, solvable parts.

Critique its own (partial) solutions and find errors.

Explore many alternative solutions. 

For some concrete examples of these reasoning trajectories, see [this blog post](https://openai.com/index/learning-to-reason-with-llms/). Notably, the long CoT used by OpenAI’s reasoning models are “internal”, meaning that they are hidden from the user when interacting with the model. Instead, the user sees a model-written summary of the long CoT; see below.

![](https://substackcdn.com/image/fetch/$s_!JJH6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c08cfd9-85a6-4079-b510-59857ae05c3e_1970x1174.png)

([source](https://openai.com/index/learning-to-reason-with-llms/))

The long CoT output of reasoning models gives us an easy way to control the inference-time compute of an LLM. If we want to spend more compute on solving a problem, we can simply generate a longer CoT. Similarly, less complex problems can be solved with a shorter CoT, thus saving compute at inference time. 

**Reasoning capabilities.** Initial reasoning models were actually less capable than standard LLMs in many ways[1](#footnote-1), but they improve the reasoning capabilities of an LLM by several orders of magnitude. For example, *o1-preview unanimously outperforms GPT-4o and even rivals the performance of human experts on most complex reasoning tasks*; see below. To achieve these results, o1-preview is evaluated using maximal inference-time compute[2](#footnote-2) and either *i)* a single output sample (solid bar) or *ii)* a majority vote among 64 parallel output samples (shaded bar). 

![Competition evals for Math (AIME 2024), Code (CodeForces), and PhD-Level Science Questions (GPQA Diamond)](https://substackcdn.com/image/fetch/$s_!O5uQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde143ac3-dbf4-476c-9524-282b23c1034c_2700x1050.png)

o1 models vs. GPT-4o on reasoning tasks (from [5])

Beyond o1-preview, **OpenAI’s o1**—*the full version of o1 that was released a few months after the preview*—places among the top 500 students in the US on the math olympiad qualification exam ([AIME 2024](https://artofproblemsolving.com/wiki/index.php/American_Invitational_Mathematics_Examination?srsltid=AfmBOopg_BQh_GIwm9fLXXJSK812QdJcW_e6uohok7JzFaFCbie0twRk)) and ranks within the 11th percentile of competitive human programmers on [Codeforces](https://arxiv.org/abs/2501.01257). For reference, GPT-4o only solved 12% of AIME problems, while o1 solves anywhere from 74% to 93% of the problems depending upon inference settings. See the figure below for a more detailed comparison between the performance of o1 and GPT-4o.

![Breakdown of the accuracy and raw score of gpt-4o vs. o1 on various competition evals](https://substackcdn.com/image/fetch/$s_!KBJp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd030dac8-57ff-4d51-a8a5-7bbbec5fc3ba_2400x1650.png)

Improvement of o1 over GPT-4o (from [5])

Similarly, **o1-mini**—*a cheaper and faster version of o1*—has impressive reasoning capabilities despite its 80% cost reduction relative to the full o1 model. This model, despite having limited world knowledge compared to o1, is especially capable at coding tasks and performs very well given its efficiency.

State-of-the-Art Reasoning Models: o3 and o3-mini

![o Series Performance](https://substackcdn.com/image/fetch/$s_!qxzS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeccad4f-894f-4593-9573-ff3285420af7_1200x675.jpeg)

Performance of OpenAI’s o3 on ARC-AGI ([source](https://arcprize.org/blog/oai-o3-pub-breakthrough))

Shortly after the announcement and release of o1 models, OpenAI announced **o3**—*the most recent model in the o1 lineage*. This model was initially just announced (not released). We were able to see the model’s performance on several notable benchmarks—*as measured by OpenAI*—but could not actually use the model. The metrics released by OpenAI were very impressive. In fact, *the performance of o3 was quite shocking to many people*. The most notable achievements of o3 are:

A score of 87.5% on the [ARC-AGI benchmark](https://arcprize.org/blog/oai-o3-pub-breakthrough)—*the “North Star” towards AGI that was left unbeaten[3](#footnote-3) for five years*—on which GPT-4o achieves 5% accuracy. o3 is the first model to exceed human-level performance of 85% on ARC-AGI.

An accuracy of 71.7% on [SWE-Bench Verified](https://openai.com/index/introducing-swe-bench-verified/) and an [Elo score](https://en.wikipedia.org/wiki/Elo_rating_system) of 2727 on Codeforces, *ranking o3 among the top 200 competitive programmers on the planet*.

An accuracy of 25.2% on EpochAI’s [FrontierMath benchmark](https://epoch.ai/frontiermath), *improving upon the previous state-of-the-art accuracy of 2.0%*[4](#footnote-4). 

However, the public did not have access to the o3 model to verify any of these results. The full o3 model still has yet to be released at the time of writing, but OpenAI did recently release a smaller version of the model—***o3-mini*** [6]. 

*“Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.”* - from [6]

Compared to other reasoning models from OpenAI, o3-mini is more cost effective and production-ready. For example, this model supports features like function calling, web search and structured outputs[5](#footnote-5). o3-mini also has multiple settings—*including low, medium and high effort*—for the amount of reasoning that it performs when solving a problem. This setting can be directly specified in the API request, and the model performs very impressively—*on par with o1 in many cases*—depending on the level of reasoning effort; see below. 

![](https://substackcdn.com/image/fetch/$s_!yL5T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F809e35bd-3da6-4382-8635-dcff356f25c0_2424x1332.png)

o3-mini performance breakdown (from [6])

In most cases, o3-mini with low reasoning effort matches the performance of o1-mini, while o3-mini with high reasoning effort exceeds the performance of all other reasoning models released by OpenAI (including the full o1 model). 

o3-mini also has better world knowledge (i.e., improved factuality), is noticeably more efficient, and scores higher in human preference studies compared to prior reasoning models; see below. In particular, authors in [6] mention that during internal A/B tests *“o3-mini delivered responses 24% faster than o1-mini, with an average response time of 7.7 seconds compared to 10.16 seconds.”* o3-mini is the most efficient model released (so far) of OpenAI’s o1-style reasoning models.

![The chart compares win rates for STEM and non-STEM tasks across AI models. "o3_mini_v43_s960_j128" (yellow) outperforms "o1_mini_chatgpt" (red baseline) in both categories, with a higher win rate for STEM tasks.](https://substackcdn.com/image/fetch/$s_!PYI2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F044cb648-2c4d-4aaa-88bb-bf4548876d24_1944x994.webp)

Win-rate of o3-mini vs. o1-mini on STEM / non-STEM prompts (from [6])

**Other model providers.** The release of o1-style models by OpenAI was quickly followed by other model providers. For example, Google recently released the experimental [Gemini-2.0 Flash Thinking](https://deepmind.google/technologies/gemini/flash-thinking/), which maintains the signature long context of Gemini models—*1M token context window*—and achieves respectable metrics on key verifiable tasks (e.g., AIME and GPQA). However, *this model still lags behind the performance of o1 and o3-mini*. 

![](https://substackcdn.com/image/fetch/$s_!kQ_a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff78afa03-d704-43f4-b001-3965969a3b84_1070x556.png)

([source](https://deepmind.google/technologies/gemini/flash-thinking/))

Very recently, a reasoning beta was announced for Grok-3 that is very compelling. As shown below, the Grok-3 reasoning model exceeds the performance of o3-mini with high reasoning efforts and even comes close to matching the full o3 model in a few cases; e.g., 96% accuracy on AIME’24, compared to the 97% accuracy of o3. Grok-3, which was trained using a [massive new compute cluster](https://www.datacenterfrontier.com/machine-learning/article/55244139/the-colossus-ai-supercomputer-elon-musks-drive-toward-data-center-ai-technology-domination), is impressive (especially given the youth of xAI). At the time of writing, the reasoning beta of Grok-3 is the closest competitor to reasoning models from OpenAI. 

![r/singularity - Grok 3 Reasoning Benchmarks](https://substackcdn.com/image/fetch/$s_!1Gxi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64bc6bd5-d713-4c5e-9740-9a5e3ec81923_640x318.png)

(from Grok-3 announcement video on X)

Benchmarks for Reasoning Models

*“Recent frontier models do so well on MATH and GSM8K that these benchmarks are no longer effective at differentiating models.”* - from [5]

Before learning more about how reasoning models work, let’s take a deeper look at their performance. To truly understand the capabilities of these models, we need to do more than just look at metrics—*we need to inspect concrete examples of the problems that these models are solving*. For example, consider [GSM8K](https://arxiv.org/abs/2110.14168) (shown below), a grade-school level math benchmark. These questions might seem trivial, but LLMs struggled to accurately solve this benchmark for [several years](https://paperswithcode.com/sota/arithmetic-reasoning-on-gsm8k).

![](https://substackcdn.com/image/fetch/$s_!yc8B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87c06563-9df0-4cd4-8e8b-62acf408ffce_2300x838.png)

Example questions from GSM8K ([source](https://huggingface.co/datasets/openai/gsm8k))

With the advent of reasoning models, this benchmark has been completely saturated—*we can no longer use it to meaningfully evaluate the best reasoning models*. Instead, we are beginning to solve much harder problems with LLMs. 

![](https://substackcdn.com/image/fetch/$s_!FsXZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95dc2906-5bef-4d7a-a234-5e833d189ba1_1900x248.png)

Example problem from AIME 2024 ([source](https://artofproblemsolving.com/wiki/index.php/2024_AIME_I_Problems))

For example, consider the [15th problem from AIME 2024](https://artofproblemsolving.com/wiki/index.php/2024_AIME_I_Problems/Problem_15), as shown above. This problem is quite complex and goes beyond the arithmetic reasoning questions found in GSM8K. There are (at least) six different ways that this problem can be solved, all of which require knowledge of advanced mathematical techniques (e.g., derivatives, [number theory](https://en.wikipedia.org/wiki/Number_theory) or [Lagrange multipliers](https://en.wikipedia.org/wiki/Lagrange_multiplier)). 

Additionally, the complex benchmarks being solved by reasoning models go beyond math! For example, GPQA [7] contains hundreds of multiple-choice questions from several scientific domains; e.g., Biology, Physics, and Chemistry. All of these questions are written by domain experts and verified to be both very difficult and “Google-proof”, meaning that non-experts struggle to solve these problems even when given sufficient time and unrestricted internet access.

*“We ensure that the questions are high-quality and extremely difficult: experts who have or are pursuing PhDs in the corresponding domains reach 65% accuracy, while highly skilled non-expert validators only reach 34% accuracy, despite spending on average over 30 minutes with unrestricted access to the web.”* - from [7]

The ARC-AGI benchmark—*described as a “material stepping stone toward AGI”*—involves a variety of grid-based puzzles in which the LLM must learn patterns among input-output grids and perfectly replicate this learned pattern on a final output example; see below. Most LLMs struggle to solve these puzzles (e.g., GPT-4o achieves an accuracy of only 5%), but reasoning models perform quite well on this benchmark—*30-90% accuracy depending on the compute budget*. 

![](https://substackcdn.com/image/fetch/$s_!CNiP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb2e0506-6107-4e23-8ef5-3e0f4bb1e6e8_1538x1062.png)

To say the least, *these are a different caliber of (non-trivial) problems that reasoning LLMs are beginning to solve*. Despite the difficulty of these benchmarks, modern reasoning models are found to be remarkably capable—*OpenAI’s o3 model is reported to achieve a score of nearly 97% on AIME 2024*. After manually inspecting some of these questions, we can truly understand the gravity of this result.

Fundamentals of Reasoning Models

“*We have found that the performance of o1 consistently improves with more reinforcement learning (train-time compute) and with more time spent thinking (test-time compute).”* - from [1]

Although the reasoning models presented above are clearly impressive, there are all closed models. So, *we have no information about how they actually work*. The only information we are given is the above quote and the plot shown below.

![](https://substackcdn.com/image/fetch/$s_!ozKr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1fe00c0c-da10-431b-8316-4ea3939e50fe_1264x645.png)

(from [5])

From this limited information, however, we can draw some useful conclusions. Mainly, there are two key components involved in scaling a reasoning model:

More training via RL.

More inference-time compute (i.e., inference-time scaling).

Although OpenAI does not reveal many of the details behind their approach to scaling these two components of a reasoning model, there is still [a lot of research](https://github.com/srush/awesome-o1) that has been published on this topic. To provide more context, let’s briefly take a look at some of this work—*along with details shared by OpenAI*—to outline some of the key concepts that underlie how reasoning models are trained and used. 

Reinforcement Learning with Verifiable Rewards

One detail that we should immediately notice about o1-style models is that they are primarily used for and evaluated on problems that are verifiable in nature; e.g., math and coding. But, *what exactly does “verifiable” mean in this context?* First, we assume that we have access to either *i)* a ground truth answer for the problem or *ii)* some rules-based technique that can be used to verify correctness. 

![](https://substackcdn.com/image/fetch/$s_!zfsl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb865992-1eee-4fdb-b98a-165f4d555e11_1774x608.png)

Verifying a math problem via exact string match

For example, we can define a ground truth final answer for most math problem—this is done in [GSM8K](https://huggingface.co/datasets/openai/gsm8k) with the `#### <answer>` syntax. Then, we can extract the final answer from the LLM’s output and compare this answer to the ground truth using a basic string match; see above. Similarly, if we have test cases prepared for a coding question, we can simply execute the code produced by our LLM and check whether the provided solution satisfies all of the test cases.

*“Reinforcement Learning with Verifiable Rewards (RLVR) can be seen as a simplified form of existing approaches for bootstrapping LM reasoning or a simpler form of RL with execution feedback, in which we simply use answer matching or constraint verification as a binary signal to train the model.” *- from [13]

Saying that a domain is “verifiable” does NOT mean that we can automatically verify arbitrary solutions to problems in this domain. Rather, we will often need access to ground truth answers—*typically obtained from humans*—for verification. 

However, there are some behaviors* *that can be verified using simple rules instead of ground truth. For example, we can determine whether a reasoning model has the correct output format, follows certain instructions, or produces outputs of a particular length (e.g., the low, medium or high reasoning effort used by o3-mini) by performing simple checks with a set of hard-coded rules. 

**Verification complexities.** Verifying an LLM’s output can become quite complex depending on the problems we are solving. Even for math problems, verifying a match between the LLM’s answer and ground truth is difficult. For example, the solution may be presented in a different form or format, leading to false negative verifications. In these cases, simple string matching may not be enough! Instead, we can prompt an LLM to tell us whether the two solutions are a match or not, which has been found to drastically reduce incorrect verifications [14]. For code, implementing verification is tough as well—*it requires constructing a data pipeline that can very efficiently execute and verify test cases within our training setup*.

*“We do not apply neural reward model in developing DeepSeek-R1-Zero, because we find that the neural reward model may suffer from reward hacking in the large-scale RL process, and retraining the reward model needs additional training resources and it complicates the whole training pipeline.”* - from [1]

**Neural verification.** Beyond the verifiable problems outlined above, we can also consider weaker forms of verification. For example, creative writing is a task that is difficult to verify. However, we can:

Train a [neural reward model](https://arxiv.org/abs/2403.13787) or verifier.

Score our LLM’s output with this model.

Use the predicted score as a reward or verification signal.

Such a setup is very similar to [reinforcement learning from human feedback (RLHF)](https://cameronrwolfe.substack.com/p/the-story-of-rlhf-origins-motivations). In this case, we are training our reward model to perform binary verification based on the correctness or quality of the model’s response[6](#footnote-6). However, using a neural verifier comes with the risk of [reward hacking](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/), especially when performing large-scale RL. The model is trained for longer and does much more exploring of the reward landscape, thus increasing the risk of reward hacking.  As a result, many recent reasoning models have avoided this approach.

**Learning from verifiable rewards.** We now understand verification, but how can verification be used to train an LLM? The idea here is simple: *we just directly use the verification result as a reward signal for training with RL*; see below. There are many different ways of implementing this idea (e.g., [process rewards](https://arxiv.org/abs/2305.20050) or [pure RL](https://www.interconnects.ai/p/openais-o1-using-search-was-a-psyop)), but they share the common theme of using RL to learn from verifiable rewards. *This is the fundamental concept upon which all modern reasoning models are based*.

![](https://substackcdn.com/image/fetch/$s_!mzxO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7334cdb5-5398-47d2-98bb-01ca41a58879_1854x726.png)

(from [13])

For a complete exposition of methods that can be used to learn from verifiable rewards with RL, check out the incredible video by [Sasha Rush](https://rush-nlp.com/) below.

Inference-Time Strategies: Chain of Thought and Decoding

There are two basic ways[7](#footnote-7) that we can increase the amount of compute that our language model is consuming at inference time:

Generate more tokens (i.e., longer output sequence).

Generate multiple outputs.

In this section, we will go into these techniques in more detail, exploring how they are practically implemented in LLMs via chains of thought and different decoding strategies; e.g., parallel versus sequential decoding.

![](https://substackcdn.com/image/fetch/$s_!NPw_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F599a636e-b0b2-4de3-84c8-3edf906bfa82_1616x882.png)

(from [8])

**Chain of thought.** We already know that reasoning models use long CoT as their medium for reasoning. Proposed in [8], a chain of thought—*at the simplest level*—is just an explanation that an LLM provides for its own output. In most cases, these explanations are written prior to the LLM generating its final answer, allowing the model to use its explanation as context when generating its answer; see above.

The long CoT used by reasoning models is much different than a standard CoT. A standard CoT is concise and human-readable. A long CoT is several thousand tokens long[8](#footnote-8). Although it can be used for interpretability purposes, the long CoT is not optimized for human readability. Rather, it is an extensive reasoning trace that approaches problem solving in a detailed manner and contains a variety of complex reasoning behaviors (e.g., backtracking and self-refinement). 

*“We have decided not to show the raw chains of thought to users… We strive to partially make up for [this decision] by teaching the model to reproduce useful ideas from the chain of thought in the answer. For the o1 model series we show a model-generated summary of the chain of thought.”* - from [5]

Additionally, reasoning models logically separate their CoT from the final output of the model. For example, OpenAI avoids exposing the long CoT directly to users and instead provides an LLM-generated summary of the long CoT to supplement the reasoning model’s final answer. Such a logical separation is fundamentally necessary due to the length of CoT. Most users will only read the final answer—*reading the entire reasoning trace would be incredibly time consuming*. 

![](https://substackcdn.com/image/fetch/$s_!mBBe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7b26d4a-0d1c-4e27-a63d-5fe7035e83b1_604x278.png)

(from [15])

**Parallel decoding.** To improve the accuracy of an LLM’s final output, we may also use parallel decoding techniques; see above. The idea here is simple: *instead of generating a single output with our LLM, we generate multiple outputs and aggregate these outputs to form a single, final answer*. This aggregation can be done in many ways; e.g., using [majority vote](https://arxiv.org/abs/2203.11171) or consensus, using [weighted voting](https://arxiv.org/abs/2206.02336), identifying the best output(s) with a [neural reward model or verifier](https://arxiv.org/abs/2408.15240) (i.e., also known as [Best-of-N or rejection sampling](https://arxiv.org/abs/2110.14168)), or [other domain-specific algorithms](https://arxiv.org/abs/2210.02441). 

The main benefit of these approaches is their simplicity and effectiveness. Scaling up parallel decoding is easy—*we just generate, verify and aggregate a larger number of outputs—*and yields meaningful boosts in performance [9, 10, 11]. Parallel decoding techniques are clearly used by o1-style models—*just look at the details of the plots provided in their blog posts (shown below)*! However, parallel decoding techniques cannot by themselves explain some of the more complex reasoning behaviors exhibited by recently released reasoning models. 

![](https://substackcdn.com/image/fetch/$s_!-0o4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37f574b5-9d41-4b11-b49a-2d6b4c9e95ee_1942x1120.png)

(from [5])

As a side note, we can also apply the idea of rejection sampling to training (i.e., training vs. test-time rejection sampling). To do this, we just:

Sample several outputs or trajectories.

Use our reward model (or other scoring mechanism) to pick the best outputs.

Train on these outputs.

This approach is commonly used in practice; e.g., LLaMA models perform several rounds of training-time rejection sampling in their post training process prior to the application of RLHF. Rejection sampling is very effective in practice and is easier to implement and scale compared to [PPO-based RLHF](https://cameronrwolfe.substack.com/p/proximal-policy-optimization-ppo). 

*“We adopt a relatively simple post-training procedure based on supervised finetuning (SFT), rejection sampling (RS), and direct preference optimization (DPO) as opposed to more complex reinforcement learning algorithms that tend to be less stable and harder to scale.”* - from [12]

**Self-refinement.** Beyond parallel decoding, we can also consider critique or self-refinement strategies for decoding. First, the LLM generates an initial response. Then, feedback—*either from the LLM or some external sourc*e—is provided for the response, and the LLM can revise its response based on the feedback. This cycle can repeat for an arbitrary number of iterations; see below for an illustration.

![](https://substackcdn.com/image/fetch/$s_!dvWP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a8ce6da-c042-4dc3-adeb-89f0f0cc1263_898x378.png)

(from [15])

Several different approaches for refinement exist, but they can be broadly categorized into two groups:

*Extrinsic*: feedback comes from some external verifier or module.

*Intrinsic*: the LLM provides feedback on its own generation.

The results and practical effectiveness of refinement are somewhat mixed. There are many successful examples of using extrinsic feedback—*such as from a verifier [16] or a code interpreter [17]*—to refine the output of an LLM. Whether intrinsic refinement is effective is highly dependent upon the quality of feedback provided by the LLM. Intrinsic refinement can work well for simple tasks [18]. However, this approach struggles to generalize to more complex tasks (e.g., math) [19]. 

*“When LLMs give relatively accurate self-examinations as rewards, they are capable of refining responses in an in-context way.”* - from [18]

Open Reasoning: DeepSeek-R1 and More

So far, we have learned about the basic concepts that allow us to instill reasoning capabilities within an LLM. However, all of the models we have learned about are closed—*we have no way of knowing how exactly these models were created*. Luckily, several open reasoning models have been recently released. The most notable of these models, which we will cover in this section, is called DeepSeek-R1 [1]. In addition to matching the performance of OpenAI’s o1, this model comes with a full technical report that provides sufficient details for replication and, therefore, completely demystifies the process needed to create a powerful reasoning model.

![](https://substackcdn.com/image/fetch/$s_!jOEt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F728166d1-a874-48ab-a2a4-ea81e0636228_1224x730.png)

(from [1])

The core idea behind DeepSeek-R1 aligns well with what we have learned for far. The model is trained with RL on verifiable tasks, where it learns to leverage long CoT to solve complex reasoning problems. Interestingly, the RL training process is the key contributor to the model’s strong reasoning capabilities. Multiple versions of this model—*DeepSeek-R1-Zero and DeepSeek-R1*—are released that have comparable reasoning capabilities. As we will see, the first of these models completely forgoes any supervised training, demonstrating that complex reasoning capabilities naturally emerge from large-scale training with RL. 

*“DeepSeek-R1-Zero, a model trained via large-scale reinforcement learning (RL) without supervised fine-tuning (SFT) as a preliminary step, demonstrates remarkable reasoning capabilities. Through RL, DeepSeek-R1-Zero naturally emerges with numerous powerful and intriguing reasoning behaviors.”* - from [1]

**DeepSeek-v3.** The creation of both DeepSeek-R1-Zero and DeepSeek-R1 begins with a powerful base model, called DeepSeek-v3 [2]. In addition to having open weights and a detailed technical report [2], this model surpasses the performance of prior open LLMs and even matches the quality of closed models; see below.

![](https://substackcdn.com/image/fetch/$s_!a08q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc26d7720-a597-49c3-82b7-5ee830132411_1846x1186.png)

(from [2])

DeepSeek-v3 is a 671 billion parameter Mixture-of-Experts (MoE) model. If you are unfamiliar with MoEs, please check out the post below, which explains the concept and provides several practical examples, including DeepSeek-v3. 

To improve inference and training efficiency, DeepSeek-v3 makes the following design choices (see [here](https://cameronrwolfe.substack.com/i/154340424/deepseek-v-and-deepseek-v) for more details):

Uses Multi-Headed Latent Attention (MLA). 

Adopts an optimized MoE structure (e.g., fine-grained and shared experts). 

Uses a multi-token prediction objective during pretraining.

Forgoes load balancing losses typically used to train MoE models. 

Decreases precision to FP8 throughout training by adopting a novel quantized training strategy that is proposed in [2]. 

For these reasons, the training of DeepSeek-v3 is very economical compared to other models—*the model is impressive in terms of both performance and efficiency*. Several prior versions of this model were released that inspire some of the design decisions made by DeepSeek-v3; e.g., see [DeepSeek-v2](https://arxiv.org/abs/2405.04434) and [DeepSeek-v2.5](https://api-docs.deepseek.com/news/news1210)[9](#footnote-9). 

DeepSeek-R1-Zero

*“We explore the potential of LLMs to develop reasoning capabilities without any supervised data, focusing on their self-evolution through a pure reinforcement learning process.” *- from [1]

The first reasoning model proposed by DeepSeek was DeepSeek-R1-Zero. This model adopts an interesting training strategy that teaches the model to reason purely via large-scale RL—*without any SFT*. The model naturally explores and learns to leverage long CoT to solve complex reasoning problems through RL. DeepSeek-R1-Zero is the first open research effort to show that reasoning capabilities can be developed without supervised training.

![](https://substackcdn.com/image/fetch/$s_!_Old!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c284b27-d0f4-4699-b4a0-24c37e8eef88_1840x882.png)

(from [22])

**RL with GRPO.** The training of DeepSeek-R1-Zero begins with the DeepSeek-v3 [2] base model. We directly finetune this base model via RL. In particular, authors in [1] select [Group Relative Policy Optimization (GRPO)](https://huggingface.co/docs/trl/main/en/grpo_trainer) [3], which is depicted in the figure above, as their RL algorithm. The selection of RL algorithms for LLM training is an open and active research topic. Traditionally, researchers have used [PPO](https://cameronrwolfe.substack.com/p/proximal-policy-optimization-ppo) for training LLMs, but there is a recent trend towards adopting simpler RL algorithms—*such as [REINFORCE](https://arxiv.org/abs/2402.14740) or [GRPO](https://arxiv.org/abs/2501.12599)*—for LLM training. The main reasons provided for the selection of GRPO in [1] are:

A reduction in the cost of RL training.

The elimination of the critic model, which is (usually) the same size as the policy model (i.e., the LLM itself). 

**Defining rewards.** Unlike most traditional work on RL with LLMs, no neural reward models—*meaning LLM-based reward models that are trained over preference data*—are used to train DeepSeek-R1-Zero. Rather, the authors use a rules-based reward system, which *i)* avoids reward hacking, *ii)* saves on compute costs[10](#footnote-10), and *iii)* is simpler to implement. There are two types of rewards used in particular:

*Accuracy reward*: evaluates whether the model’s response is correct.

*Format reward*: enforces a desired format on the model’s output.

DeepSeek-R1-Zero is trained purely on automatically verifiable tasks, such as math and coding problems. For math problems with deterministic results, the model can provide its answer in a specified format, allowing us to verify via basic string matching. Similarly, coding problems can be verified by executing the code produced by the LLM in a sandbox over predefined test cases.

*“The neural reward model may suffer from reward hacking in the large-scale reinforcement learning process, and retraining the reward model needs additional training resources and it complicates the whole training pipeline.”* - from [1]

As mentioned above, the format reward provides a positive training signal when the model produces an output that uses the correct format or template. The format used in [1] simply places the model’s long CoT—*or the thinking / reasoning process*—between two special tokens: `<think>` and `</think>`. The model then produces its answer separately—*between the *`<answer>`* and *`</answer>`* tags*—after the completion of the reasoning process; see below for an illustration.

![](https://substackcdn.com/image/fetch/$s_!lZD6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bdc9fc1-4032-41ba-9d7a-946f4826f826_1840x454.png)

(from [1])

**Learning via RL.** Despite using no SFT, DeepSeek-R1-Zero shows clear progress in its reasoning capabilities throughout the RL training process. The model’s performance on AIME 2024 is plotted below as training progresses. Here, the model’s performance gradually improves, eventually reaching parity with o1-preview[11](#footnote-11). After training completes, DeepSeek-R1-Zero has improved from an initial performance of 15.6% to 71.0%—*or 86.7% when using majority voting with 16 votes*—on AIME 2024! Such results mirror the trends in performance we see with closed reasoning models—*DeepSeek-R1-Zero achieves impressive performance after RL training and can further improve its performance via parallel decoding strategies*. 

![](https://substackcdn.com/image/fetch/$s_!8rFM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe19787e1-df29-413b-8ab3-7ed137eca9d9_1844x1028.png)

(from [1])

A full performance comparison between DeepSeek-R1-Zero and o1 models is provided in the table below. DeepSeek-R1 matches or exceeds the performance of o1-mini in most cases and performs comparably to o1-preview on several tasks. However, reasoning models from OpenAI perform much better in the coding domain—*DeepSeek-R1-Zero is clearly a less powerful coding model*. As we will soon see, this problem is fixed in DeepSeek-R1 (the follow-up model).

![](https://substackcdn.com/image/fetch/$s_!5Xef!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba93d001-c99e-4b80-a371-b97d92ea1adc_2008x506.png)

(from [1])

**What is happening here?** Clearly, DeepSeek-R1-Zero gains impressive reasoning capabilities from the RL training process outlined in [1]. However, *the dynamics of the model’s learning process are also quite observable*! Because we perform no SFT-style training, we can closely monitor the progression of the model’s reasoning strategy throughout the RL training process. As shown below, DeepSeek-R1-Zero learns to leverage more “thinking time”—*or just generate progressively longer chains of thought*—to improve its reasoning process as training progresses. The model naturally learns to leverage more test-time compute to solve harder problems!

![](https://substackcdn.com/image/fetch/$s_!COPD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36e006bb-5959-485b-bb4a-d45b235a8a9d_1800x1004.png)

(from [1])

Authors in [1] also observe several interesting tendencies that emerge naturally during training with RL. For example, the model develops an ability to reflect upon its own solutions by revisiting and evaluating prior components of its reasoning process. Similarly, the model begins to explicitly test out and explore alternative solutions or approaches during the problem solving process. This behavior is not explicitly programmed—*it arises naturally during training with RL*! 

*“The self-evolution of DeepSeek-R1-Zero is a fascinating demonstration of how RL can drive a model to improve its reasoning capabilities autonomously.”* - from [1]

At the most basic level, the RL environment constructed in [1] allows the model to explore different strategies for arriving at a correct—*as determined by verification*—final solution. During exploration, we reward the model for:

Using the correct reasoning template or structure.

Producing a correct final solution.

From these rewards alone, the model learns how to solve complex reasoning problems. We do not explicitly need to teach the model how to decompose problems, search for a solution, perform backtracking, or evaluate its own line of thought. Instead, we just provide the correct incentives (or rewards) to the model during the training process. Then, the LLM can autonomously learn necessary behaviors for solving problems via an RL-based “self-evolution” process. 

DeepSeek-R1

DeepSeek-R1-Zero shows us that LLMs can develop impressive reasoning capabilities from pure RL with no SFT, but this model has some minor bugs. For example, its readability is poor[12](#footnote-12) and it incorrectly mixes languages together. Put simply, DeepSeek-R1-Zero is very good at reasoning, *but it lacks some of the desirable properties of a well-[aligned](https://cameronrwolfe.substack.com/p/the-history-of-open-source-llms-imitation) LLM*. As a solution, authors in [1] propose a new, multi-stage training process that integrates some “cold start” SFT data into training along with some other tricks. This training pipeline is used to create DeepSeek-R1, an LLM that is both aligned and capable of complex reasoning.

Similarly to DeepSeek-R1-Zero, we begin with DeepSeek-v3 as a base model. Then, DeepSeek-R1 undergoes four stages of training, including two SFT phases and two RL phases. The purpose of the SFT phases is to provide a better starting point for exploration during each of the RL phases. This training pipeline is one of the key contributions of [1]—*it provides an effective recipe for combining reasoning-style training with the standard post training recipe for LLMs. *Let’s take a deeper look at each stage of the training recipe used for DeepSeek-R1. 

*“To prevent the early unstable cold start phase of RL training from the base model, for DeepSeek-R1 we construct and collect a small amount of long CoT data to fine-tune the model as the initial RL actor.”* - from [1]

**Phase One: Cold Start (or Reasoning-Oriented SFT).** Prior to RL training, R1 is trained via SFT over a small dataset of long CoT examples, which is referred to in [1] as “cold start” data. There are a few different approaches that we can use to collect this cold start data:

Prompt a model (e.g., DeepSeek-v3) to produce long CoT data, either with few-shot examples or by instructing the model to generate detailed answers with accompanied reflection and verification.

Use the R1-Zero model to generate a large number of long CoT outputs, then ask humans to post-process and select the model’s best outputs.

Authors in [1] combine these approaches to collect “thousands of cold-start data” on which DeepSeek-v3 is finetuned directly via SFT. Because we are using long CoT data, *this is a reasoning-oriented finetuning process*. From this cold start data, the model learns a viable (initial) template for solving reasoning problems. 

The data used for reasoning-oriented SFT introduces a human prior into DeepSeek-R1’s training process. We can explicitly select the style and pattern of data from which the model learns during this stage. For example, authors in [1] mention that they structure this data to include summaries of each long CoT, thus teaching the model to summarize its entire reasoning process prior to providing its final answer. This data serves as a seed for the RL training process—*the model begins its self-exploration by matching the style of the SFT training data.*

**Stage Two: Reasoning-Oriented RL.** After SFT, we just repeat the large-scale RL training process proposed by R1-Zero to enhance the underlying model’s ability to handle reasoning-intensive tasks. The only change made for DeepSeek-R1 is the addition of a language consistency reward, calculated as the portion of the model’s output written in the desired target language. This language consistency reward is found in [1] to slightly deteriorate the model’s reasoning capabilities. However, language consistency improves the overall alignment of the resulting model with human preferences—*the model’s output is more fluent and readable*.

**Stage Three: Rejection sampling.** After the convergence of reasoning-oriented RL, we use the resulting model to collect a large and diverse SFT dataset. Unlike the initial cold start SFT phase, however, we collect more than just reasoning-oriented data. Namely, we augment the reasoning data with general purpose data so that the model can learn from a broader set of problems and domains. 

To collect more reasoning data, authors in [1]:

Curate a diverse set of reasoning-based prompts.

Generate candidate trajectories[13](#footnote-13) using the model from phase two.

Perform rejection sampling—*or filter and select the top trajectories based on the quality and correctness or each trajectory*. 

This is the same training-time rejection sampling process that we learned about earlier in this post! Interestingly, we rely upon more than rules-based techniques for verification in this phase. We also incorporate additional data from non-verifiable domains by using DeepSeek-v3 as a [generative reward model](https://arxiv.org/abs/2408.15240) or weak verifier. After applying heuristic filtering (e.g., removing outputs with language mixing or long paragraphs), we arrive at a final set of 600K reasoning trajectories. 

*“We reuse portions of the SFT dataset of DeepSeek-V3. For certain non-reasoning tasks, we call DeepSeek-V3 to generate a potential chain-of-thought before answering the question by prompting.”* - from [1]

The SFT dataset from this stage includes a substantial ratio of non-reasoning data (e.g., writing or translation examples). We source this data from the same post training dataset used for DeepSeek-v3. However, the data is augmented by asking DeepSeek-v3 to generate a long CoT to explain the outputs of complex queries—*simpler queries, however, are not given any CoT*. A total of 200K non-reasoning examples are collected, forming an SFT dataset of 800K examples. 

**Stage Four: General-purpose RLHF.** The final training stage of DeepSeek-R1 aligns the model with human preferences while continuing to hone its reasoning abilities. Similarly to the prior stage, we train the model over a combination of reasoning-based and general purpose data. In particular, we train the model using RL with a combination of different rewards for each type of data:

Rules-based rewards (same as R1-Zero) for reasoning-based problems. 

Neural reward models—*trained over human preference pairs, just as in standard RLHF*—for general purpose data.

DeepSeek-R1 is aligned to be more helpful and harmless on general purpose data. These are two [very common alignment criteria](https://arxiv.org/abs/2204.05862) used in LLM research. Each of these criteria are modeled with a separate neural reward model that is trained over a (supervised) dataset of human preferences. Helpfulness rewards are only measured over the final answer of the model (i.e., excluding the long CoT), while harmless rewards consider the model’s entire output trajectory[14](#footnote-14). By combining rules and preference-based rewards, DeepSeek-R1 can be aligned to human preferences while maintaining strong reasoning performance.

![](https://substackcdn.com/image/fetch/$s_!0Wcf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d42ce87-35e7-4af2-8a45-cf348df75132_1918x1094.png)

(from [1])

**How does it perform?** As shown above, R1 matches or surpasses the performance of o1 on most reasoning tasks. Unlike R1-Zero, R1 also has reasonably strong coding abilities. On general purpose tasks, R1 continues to perform well as a result of its hybrid training pipeline. In general, R1 is a very capable model that seems to be on par with OpenAI’s o1 and can solve a wide variety of tasks—*including both traditional and reasoning-oriented tasks*—with high accuracy.

One interesting observation about this model (and other reasoning models) is that it performs poorly on instruction following benchmarks (e.g., [IF-Eval](https://arxiv.org/abs/2311.07911)) compared to standard LLMs. Currently, *reasoning models seem to be worse than standard LLMs at following instructions*. In the future, I personally believe this trend is likely to reverse. In theory, reasoning models should be capable of leveraging their thought process to better interpret and adhere to a prompt provided by a human user. For example, [deliberative alignment](https://arxiv.org/abs/2412.16339) follows a somewhat similar approach.

**Is SFT necessary?** R1-Zero emphasizes the ability to train strong reasoning models without SFT, while the full R1 model uses several SFT phases to obtain a stronger, final model. So, we might begin to wonder: *Should we use SFT of not? *

![](https://substackcdn.com/image/fetch/$s_!Vw21!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6b1fbd1-3f9b-4983-8914-1a93d2d2fa87_2388x1154.png)

Is SFT necessary for reasoning models?

For a standard LLM, SFT provides a high-quality starting point for RLHF. If we applied RLHF directly to the base model, the learning process would be much less efficient. Data for SFT is either synthetically generated or manually created by humans. Generally, collecting data for SFT is expensive (both in terms of time and money). *We have to manually write a good response from scratch for the LLM*!

Collecting such SFT data for reasoning models is more difficult due to their long CoT. Asking humans to manually create long CoT data would be time consuming and expensive! Our only option is to generate this data synthetically, but:

Generating this particular style of output with a model may still be hard.

Correctly verifying such long outputs is difficult.

Given the additional complexity of collecting SFT data for reasoning models, authors in [1] first try to avoid SFT altogether! From these experiments, we see that such reasoning abilities naturally emerge from pure RL—*this is an incredible discovery*! However, the resulting model has several shortcomings (e.g., language mixing). When we train over some SFT prior to RL (i.e., a “cold start”), we provide a better prior to RL, which *i)* eliminates instability during the initial phases of RL training, *ii)* speeds up up training and *iii)* improves model quality. So, SFT is not completely necessary, *but it is still practically useful if we have the data*!

Distilled Models

![](https://substackcdn.com/image/fetch/$s_!9nuA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e1abb7a-4035-421b-bcbe-35ccfdb71e47_1248x534.png)

Illustration of the knowledge distillation process ([source](https://arxiv.org/abs/2006.05525))

Beyond DeepSeek-R1, authors in [1] release a series of dense models that are distilled from R1. The [distillation process](https://arxiv.org/abs/2402.13116) is found to significantly enhance the reasoning capabilities of smaller and more efficient models. The full DeepSeek-R1 model is large (i.e., a 671 billion parameter [Mixture-of-Experts model](https://cameronrwolfe.substack.com/i/154340424/deepseek-v-and-deepseek-v)), so these distilled models are practically useful—*they are* *comparable to R1 but more cost sensitive and easier to use*. Additionally, the release of these distilled models matches recent trends in closed reasoning models (e.g., o1-mini and o3-mini). 

![](https://substackcdn.com/image/fetch/$s_!iwuY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8aa60aba-ec97-40c9-b10a-1b1a262ff251_1222x574.png)

(from [1])

**Distilling R1.** To create these models, we begin with several sizes of two base models[15](#footnote-15)—*Qwen-2.5 [20] and LLaMA-3 [21]*. We then train the base models via SFT over the 800,000 supervised training examples curated in the third stage of the training pipeline for DeepSeek-R1—*that’s it*!

This is a simple knowledge distillation pipeline, *but the results are impressive*. As shown above, the distilled Qwen2.5-14B model outperforms [QwQ-32B-Preview](https://qwenlm.github.io/blog/qwq-32b-preview/), which was the best open reasoning model prior to the release of R1. Additionally, even the smallest distilled models outperform standard closed LLMs that are not optimized for reasoning (e.g., GPT-4o), while the 32 and 70 billion parameter distilled models exceed the performance of o1-mini on most benchmarks.

*“Distilling more powerful models into smaller ones yields excellent results, whereas smaller models relying on the large-scale RL require enormous computational power and may not even achieve the performance of distillation.”* - from [1]

**Distillation versus RL.** Although we see that distillation is effective in the discussion above, we might wonder whether we could get better results by just directly applying the large-scale RL training process used by DeepSeek-R1 to these smaller models. Interestingly, authors in [1] observe that distilling the Qwen2.5-32B base model from R1—*using the distillation approach described above*—outperforms directly training this model via large-scale RL; see below.

![](https://substackcdn.com/image/fetch/$s_!IhEm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbc4ed3b-81bd-44a2-b8b7-5c0ec792f3cd_2464x406.png)

(from [1])

In other words, the reasoning patterns discovered by large models are crucial for improving the reasoning capabilities of these smaller, dense models. However, authors in [1] do make the following additional points:

It is possible that the performance of distilled models could be further improved via added training with RL.

“Advancing beyond the boundaries of intelligence”—*or creating new reasoning models that even exceed the performance of models like DeepSeek-R1*—will still require powerful base models and large-scale training with RL.

**Other distilled reasoning models.** Given the simplicity of training high-quality reasoning models via distillation, a wide variety of reasoning models were released by the research community following the proposal of R1. Some of the most notable releases are:

[Sky-T1](https://novasky-ai.github.io/posts/sky-t1/) and [Sky-T1-Flash](https://novasky-ai.github.io/posts/reduce-overthinking/)

[Bespoke Stratos](https://www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation)

[LIMO](https://arxiv.org/abs/2502.03387)

[S1](https://arxiv.org/abs/2501.19393)

[RedStar](https://arxiv.org/abs/2501.11284)

There are many more models that have been released as well! The current pace of reasoning model releases is reminiscent of the post-LLaMA era of LLM research. After the release of a powerful open base model (i.e., [LLaMA](https://cameronrwolfe.substack.com/p/llama-llms-for-everyone)), we saw a wide variety of model variants released that were based on this model (e.g., [Alpaca](https://crfm.stanford.edu/2023/03/13/alpaca.html), [Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/), [Koala](https://bair.berkeley.edu/blog/2023/04/03/koala/) and many more). Now, we have access to a strong open reasoning model, as we are seeing a very similar trend! The research in this area is very interesting and deserving of its own post—*stay tuned*!

Key Emerging Trends

We have now learned about a variety of reasoning models, beginning with closed models like o1 or o3 and ending with a fully-outlined replication of these models in DeepSeek-R1. As we have learned about this research, there are a few common trends that begin to emerge. These trends, outlined below, make some important distinctions between research on reasoning models and standard LLMs. 

**Long CoT (and inference-time scaling).** The key distinction between reasoning models and standard LLMs is their output structure. Instead of just directly generating a final answer (with an optional concise explanation), reasoning models generate a long CoT that describes their reasoning process in great detail. This long CoT can be of variable length, enabling controllable compute costs at inference time: *longer CoT = more tokens = more compute*. In this way, using more compute at inference time—*by generating a longer CoT*—has become a tool that can allow users to dynamically improve a model’s reasoning capabilities. 

**Self-evolution through RL.** Obviously, the ability of LLMs to execute complex reasoning strategies within their long CoT is new and exciting. From recent research, we learn that the key contributor to the development of these special abilities is large-scale RL training. We see in [1] that such reasoning capabilities naturally emerge during RL if the model is correctly incentivized, usually via rules-based rewards that are deterministic and reliable. Additionally, we can further improve a model’s reasoning capabilities by using more compute for training via RL—*this is yet another scaling law that we can leverage*!

**Less supervision.** The dependence of reasoning models upon human supervision is less pronounced relative to standard LLMs. In particular, rewards during RL training are derived primarily from rules-based systems, instead of relying upon human preferences. Of course, reasoning models still have several areas of dependence upon human supervision; e.g., the base model is trained with human-curated data and verification relies upon human-provided ground truth labels. However, there is still a big push by reasoning models like R1 (and especially R1-Zero) to demonstrate that reasoning capabilities can develop autonomously. 

**Distillation is effective.** Now that we have access to large and powerful reasoning models, we can distill the capabilities of these models into smaller, dense models using simple strategies! This finding has led to an explosion of research in this area, and we are likely to see many more efficient and distilled reasoning models released in the near future. One key question in this area is whether smaller models will generalize or [struggle to fully match](https://arxiv.org/abs/2305.15717) the breadth of their teachers.

*“When evaluating DeepSeek-R1, we observe that it is sensitive to prompts. Few-shot prompting consistently degrades its performance.”* - from [1]

**New problems to solve.** Above all else, the advent of reasoning models has raised a variety of new (and interesting!) questions that we need to solve:

How do we handle safety training for long CoT?

What is the best balance between general / reasoning capabilities?

What is the optimal role of SFT in training reasoning models?

How do we minimize “overthinking” in long CoT?

How do we handle efficient hosting of reasoning models?

As mentioned at the beginning of this post, reasoning models are a truly new type of LLM that will force us to rethink existing frameworks. Solidified techniques that have been used for years (e.g., few-shot prompting) are becoming obsolete for these new models. *The field of LLM research is re-inventing itself once again*.

New to the newsletter?

Hi! I’m [Cameron R. Wolfe](https://cameronrwolfe.me/), Deep Learning Ph.D. and Machine Learning Scientist at [Netflix](https://research.netflix.com/research-area/nlp-and-conversations). This is the Deep (Learning) Focus newsletter, where I help readers better understand important topics in AI research. If you like the newsletter, please subscribe, share it, or follow me on [X](https://twitter.com/cwolferesearch) and [LinkedIn](https://www.linkedin.com/in/cameron-r-wolfe-ph-d-04744a238/)!

[Subscribe now](https://cameronrwolfe.substack.com/subscribe?)

Bibliography 

[1] Guo, Daya, et al. "Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning." *arXiv preprint arXiv:2501.12948* (2025).

[2] Liu, Aixin, et al. "Deepseek-v3 technical report." *arXiv preprint arXiv:2412.19437* (2024).

[3] Shao, Zhihong, et al. "Deepseekmath: Pushing the limits of mathematical reasoning in open language models." *arXiv preprint arXiv:2402.03300* (2024).

[4] OpenAI. “Introducing OpenAI o1-preview” *[https://openai.com/index/introducing-openai-o1-preview/](https://openai.com/index/introducing-openai-o1-preview/) *(2024).

[5] OpenAI. “Learning to Reason with LLMs” *[https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)* (2024).

[6] OpenAI. “OpenAI o3-mini” *[https://openai.com/index/openai-o3-mini/](https://openai.com/index/openai-o3-mini/) *(2025).

[7] Rein, David, et al. "Gpqa: A graduate-level google-proof q&a benchmark." arXiv preprint arXiv:2311.12022 (2023).

[8] Wei, Jason, et al. "Chain-of-thought prompting elicits reasoning in large language models." Advances in neural information processing systems 35 (2022): 24824-24837.

[9] Zelikman, Eric, et al. "Star: Bootstrapping reasoning with reasoning." Advances in Neural Information Processing Systems 35 (2022): 15476-15488.

[10] Gulcehre, Caglar, et al. "Reinforced self-training (rest) for language modeling." arXiv preprint arXiv:2308.08998 (2023).

[11] Nakano, Reiichiro, et al. "Webgpt: Browser-assisted question-answering with human feedback." arXiv preprint arXiv:2112.09332 (2021).

[12] Dubey, Abhimanyu, et al. "The llama 3 herd of models." arXiv preprint arXiv:2407.21783 (2024).

[13] Lambert, Nathan, et al. "Tulu 3: Pushing frontiers in open language model post-training." arXiv preprint arXiv:2411.15124 (2024).

[14] Bespoke Labs. “Bespoke-Stratos: The unreasonable effectiveness of reasoning distillation” *[https://www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation](https://www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation) *(2025).

[15] Welleck, Sean, et al. "From decoding to meta-generation: Inference-time algorithms for large language models." *arXiv preprint arXiv:2406.16838* (2024).

[16] Aggarwal, Pranjal, Bryan Parno, and Sean Welleck. "AlphaVerus: Bootstrapping formally verified code generation through self-improving translation and treefinement." *arXiv preprint arXiv:2412.06176* (2024).

[17] Chen, Xinyun, et al. "Teaching large language models to self-debug." *arXiv preprint arXiv:2304.05128* (2023).

[18] Wang, Yifei, et al. "A Theoretical Understanding of Self-Correction through In-context Alignment." *arXiv preprint arXiv:2405.18634* (2024).

[19] Huang, Jie, et al. "Large language models cannot self-correct reasoning yet." *arXiv preprint arXiv:2310.01798* (2023).

[20] Yang, An, et al. "Qwen2. 5 technical report." *arXiv preprint arXiv:2412.15115* (2024).

[21] Dubey, Abhimanyu, et al. "The llama 3 herd of models." *arXiv preprint arXiv:2407.21783* (2024).

[22] Shao, Zhihong, et al. "Deepseekmath: Pushing the limits of mathematical reasoning in open language models." *arXiv preprint arXiv:2402.03300* (2024).

[1](#footnote-anchor-1)

For example, o1-preview did not have the ability to upload files, could not understand other modalities of data (e.g., images), and had no web search capabilities.

[2](#footnote-anchor-2)

Although the details of how OpenAI controls the amount of inference-time compute used by o1-style models are not clear, it seems from [their blog post](https://openai.com/index/learning-to-reason-with-llms/) that these models have multiple “settings” for the amount of compute that they can use at inference time. These settings are likely related to the length of the model’s long CoT, so high inference-time compute settings would simply generate very long chains of thought. 

[3](#footnote-anchor-3)

Technically, this benchmark is still unbeaten because o3 exceeded the maximum computational budget when achieving >85% accuracy. 

[4](#footnote-anchor-4)

This benchmark was described by [Terence Tao](https://en.wikipedia.org/wiki/Terence_Tao) as likely to be unsolved by AI systems for “several years at least”. There has been some recent questioning of OpenAI’s performance on this benchmark due to [conflict of interest](https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/) between OpenAI and the organization that created this benchmark ([EpochAI](https://epoch.ai/)). 

[5](#footnote-anchor-5)

Notably, o3-mini does NOT have vision support, unlike o1. 

[6](#footnote-anchor-6)

In contrast, RLHF trains the reward model over various kinds of human preferences, usually via a [ranking loss](https://gombru.github.io/2019/04/03/ranking_loss/). 

[7](#footnote-anchor-7)

In addition to these two techniques, we could also perform some sort of search (e.g., [monte carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search))—see [here](https://arxiv.org/abs/2405.00451) for an example. However, we can also categorize search-based methods as generating more tokens at inference time. 

[8](#footnote-anchor-8)

The length of a long CoT may vary depending on model settings (e.g., OpenAI provides several settings for “reasoning effort”) or problem difficulty. 

[9](#footnote-anchor-9)

There is also a [DeepSeek-v1 model](https://arxiv.org/abs/2401.02954), but this model is dense (i.e., not an MoE) and much different from the model family that is used for DeepSeek-R1. 

[10](#footnote-anchor-10)

The compute savings come from the fact that we do not have to train (or run inference on) any reward models. 

[11](#footnote-anchor-11)

See [here](https://platform.openai.com/docs/models#o1) for a full list of OpenAI’s o1 models. For clarity, the `o1-0912` model mentioned in [1] is the same as the `o1-preview` model.  

[12](#footnote-anchor-12)

For example, the model lacks markdown formatting and highlighting within its answers, which is a common feature for modern LLMs. 

[13](#footnote-anchor-13)

In [1], authors refer to the long CoT outputs generated by the DeepSeek-R1 model variants as “trajectories”. 

[14](#footnote-anchor-14)

Notably, this is in direct contrast to the (original) approach adopted by OpenAI. o1-style models have their long CoT hidden from the end user, and these reasoning traces do not undergo any safety training. The rationale for this strategy is to allow the model to be more transparent in its trajectory, which improves interpretability. 

[15](#footnote-anchor-15)

The exact models used are Qwen2.5-Math-1.5B, Qwen2.5-Math-7B, Qwen2.5-14B, Qwen2.5-32B, Llama-3.1-8B, and Llama-3.3-70B-Instruct. Notably, we do not always start with the base model—*many of these models have undergone post training*!
