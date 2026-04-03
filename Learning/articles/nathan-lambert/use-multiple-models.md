# Use multiple models

**Source:** https://www.interconnects.ai/p/use-multiple-models
**Ingested:** 2026-04-02
**Tags:** rlhf, reinforcement-learning, llms

---

I’ll start by explaining my current AI stack and how it’s changed in recent months. For chat, I’m using a mix of:

**GPT 5.2 Thinking / Pro**: My most frequent AI use is getting information. This is often a detail about a paper I’m remembering, a method I’m verifying for my [RLHF Book](https://rlhfbook.com/), or some other niche fact. I know GPT 5.2 can find it if it exists, and I use Thinking for queries that I think are easier and Pro when I want to make sure the answer is right. Particularly GPT Pro has been the indisputable king for research for quite some time — Simon Willison’s coining of it as his “[research goblin](https://simonwillison.net/2025/Sep/6/research-goblin/)” still feels right.

I never use GPT 5 without thinking or other OpenAI chat models. Maybe I need to invest more in custom instructions, but the non-thinking models always come across a bit sloppy relative to the competition out there and I quickly churn. I’ve heard gossip that the Thinking and non-Thinking GPT models are even developed by different teams, so it would make sense that they can end up being meaningfully different.

I also rarely use Deep Research from any provider, opting for GPT 5.2 Pro and more specific instructions. In the first half of 2025 I almost exclusively used ChatGPT’s thinking models — Anthropic and Google have done good work to win back some of my attention.

**Claude 4.5 Opus**: Chatting with Claude is where I go for basic code questions, visualizing simple data, and getting richer feedback on my work or decisions. Opus’s tone is particularly refreshing when trying to push the models a bit (in a way that GPT 4.5 used to provide for me, as I was a power user of that model in H1 2025). Claude Opus 4.5 isn’t particularly fast relative to a lot of models out there, but when you’re used to using the GPT Thinking models like me, it feels way faster (even with extended thinking always on, as I do) and sufficient for this type of work.

**Gemini 3 Pro**: Gemini is for everything else — explaining concepts I know are well covered in the training data (and minor hallucinations are okay, e.g. my former Google rabbit holes), multimodality, and sometimes very long-context capabilities (but GPT 5.2 Thinking took a big step here, so it’s a bit closer). I still open and use the Gemini app regularly, but it’s a bit less locked-in than the other two.

Relative to ChatGPT, sometimes I feel like the search mode of Gemini is a bit off. It could be a product decision with how the information is presented to the user, but GPT’s thorough, repeated search over multiple sources instills a confidence I don’t get from Gemini for recent or research information.

**Grok 4: **I use Grok ~monthly to try and find some piece of AI news or Alpha I recall from browsing X. Grok is likely underrated in terms of its intelligence (particularly Grok 4 was an impressive technical release), but it hasn’t had sticky product or differentiating features for me.

For images I’m using a mix of mostly **Nano Banana Pro** and sometimes **GPT Image 1.5** when Gemini can’t quite get it. 

For coding, I’m primarily using **Claude Opus 4.5** in Claude Code, but still sometimes find myself needing OpenAI’s Codex or even multi-LLM setups like [Amp](https://ampcode.com/). Over the holiday break, Claude Opus helped me update all the plots for [The ATOM Project](https://atomproject.ai/), which included substantial processing of our raw data from scraping HuggingFace, perform substantive edits for the RLHF Book (where I felt it was a quite good editor when provided with detailed instructions on what it should do), and other side projects and life organization tasks. I recently published a piece explaining my current obsession with Claude Opus 4.5, I recommend you read it if you haven’t had the chance:

![](https://substackcdn.com/image/fetch/$s_!djof!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc52e8097-8f3d-4f7e-808b-2f4ad37f3b52_720x720.png)Interconnects

Claude Code Hits Different

There is an incredible amount of hype for Claude Code with Opus 4.5 across the web right now, which I for better or worse entirely agree with. Having used coding agents extensively for the past 6-9 months, where it felt like sometimes OpenAI’s Codex was the best and sometimes Claude, there was some meaningful jump over the last few weeks. The jump is we…

Read more

3 months ago · 39 likes · 19 comments · Nathan Lambert

A summary of this is that I pay for the best models and greatly value the marginal intelligence over speed — particularly because, for a lot of the tasks I do, I find that the models are *just* starting to be able to do them well. As these capabilities diffuse in 2026, speed will become more of a determining factor in model selection.

 had a post on X with a nice graphic that reflected a very similar usage pattern:

[Share](https://www.interconnects.ai/p/use-multiple-models?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Across all of these categories, it doesn’t feel like I could get away with just using one of these models without taking a substantial haircut in capabilities. This is a very strong endorsement for the notion of AI being [jagged](https://helentoner.substack.com/p/taking-jaggedness-seriously) — i.e. with very strong capabilities spread out unevenly — while also being a bit of an unusual way to need to use a product. Each model is jagged in its own way. Through 2023, 2024, and the earlier days of modern AI, it quite often felt like there was always just one winning model and keeping up was easier. Today, it takes a lot of work and fiddling to make sure you’re not missing out on capabilities.

The working pattern that I’ve formed that most reinforces this using multiple models era is how often my problem with an AI model is solved by passing the same query to a peer model. Models get stuck, some can’t find bugs, some coding agents keep getting stuck on some weird, suboptimal approach, and so on. In these cases, it feels quite common to boot up a peer model or agent and get it to unblock project.

This multi-model approach or agent-switching happening occasionally would be what I’d expect, but with it happening regularly it means that the models are actually all quite close to being able to solve the tasks I’m throwing at them — they’re just not quite there. The intuition here is that if we view each task as having a probability of success, if said the probability was low for each model, switching would almost always fail. For switching to *regularly* solve the task, each model must have a fairly high probability of success.

For the time being, it seems like tasks at the frontier of AI capabilities will always keep this model-switching meta, but it’s a moving suite of capabilities. The things I need to switch on now will soon be solved by all the next-generation of models.

I’m very happy with the value I’m getting out of my hundreds of dollars of AI subscriptions, and you should likely consider doing the same if you work in a domain that sounds similar to mine.

Interconnects is a reader-supported publication. Consider becoming a subscriber.

On the opposite side of the frontier models pushing to make current cutting edge tasks 100% reliable are open models pushing to undercut the price of frontier models. The coding plans on open models tend to cost 10X (or more) less than the frontier lab plans. It’s a boring take, but for the next few years I expect this gap to largely remain steady, where a lot of people get an insane value out of the cutting edge of models. It’ll take longer for the open model undercut to hit the frontier labs, even though from basic principles it looks like a precarious position for them to be in, in terms of costs of R&D and deployment. Open models haven’t been remotely close to Claude 4.5 Opus or GPT 5.2 Thinking in my use.

The other factor is that 2025 gave us all of Deep Research agents, code/CLI agents, search (and Pro) tool use models, and there will almost certainly be new form factors we end up using almost every day in released 2026. Historically, closed labs have been better at shipping new products into the world, but with better open models this should be more diffused, as good product capabilities are very diffuse across the tech ecosystem.  To capitalize on this, you need to invest time (and money) trying all the cutting-edge AI tools you can get your hands on. Don’t be loyal to one provider.

![](https://substackcdn.com/image/fetch/$s_!pt_9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa87c6753-015d-496a-913c-9fa03b0d14eb_2848x1504.png)
