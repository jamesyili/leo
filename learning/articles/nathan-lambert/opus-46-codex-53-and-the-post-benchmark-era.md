# Opus 4.6, Codex 5.3, and the post-benchmark era

**Source:** https://www.interconnects.ai/p/opus-46-vs-codex-53
**Ingested:** 2026-04-02
**Tags:** rlhf, reinforcement-learning, llms

---

Last Thursday, February 5th, both OpenAI and Anthropic unveiled the next iterations of their models designed as coding assistants, [GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) and [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), respectively. Ahead of this, Anthropic had a firm grasp of the mindshare as everyone collectively [grappled with the new world of agents](https://www.interconnects.ai/p/get-good-at-agents), primarily driven by a [Claude Code with Opus 4.5](https://www.interconnects.ai/p/claude-code-hits-different)-induced step change in performance. This post doesn’t unpack how software is changing forever, [Moltbook](https://thezvi.substack.com/p/welcome-to-moltbook) is showcasing the future, ML research is accelerating, and the many broader implications, but rather how to assess, live with, and prepare for new models. The fine margins between Opus 4.6 and Codex 5.3 will be felt in many model versions this year, with Opus ahead in this matchup on usability.

[Share](https://www.interconnects.ai/p/opus-46-vs-codex-53?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Going into these releases I’d been using Claude Code extensively as a general computer agent, with some software engineering and a lot of data analysis, automation, etc. I had dabbled with Codex 5.2 (usually on xhigh, maximum thinking effort), but found it not to quite work for me among my broad, horizontal set of tasks.

For the last few days, I’ve been using both of the models much more evenly. I mean this as a great compliment, but Codex 5.3 feels much more Claude-like, where it’s much faster in its feedback and much more capable in a broad suite of tasks from git to data analysis (previous versions of Codex, including up to 5.2, regularly failed basic git operations like creating a fresh branch). Codex 5.3 takes a very important step towards Claude’s territory by having better product-market fit. This is a very important move for OpenAI and between the two models, Codex 5.3 feels far more different than its predecessors.

OpenAI’s latest GPT, with this context, keeps an edge as a better *coding model*. It’s hard to describe this general statement precisely, and a lot of it is based on reading others’ work, but it seems to be a bit better at finding bugs and fixing things in codebases, such as the [minimal algorithmic examples](https://github.com/natolambert/rlhf-book/pull/243) for my RLHF Book. In my experience, this is a minor edge, and the community thinks that this is most apparent in complex situations (i.e. not most vibe-coded apps). 

As users become better at supervising these new agents, having the best top-end ability in software understanding and creation could become a meaningful edge for Codex 5.3, but it is not an obvious advantage today. Many of my most trusted friends in the AI space swear by Codex because it can be just this tiny bit better. I haven’t been able to unlock it.

Switching from Opus 4.6 to Codex 5.3 feels like I need to babysit the model in terms of more detailed descriptions when doing somewhat mundane tasks like “clean up this branch and push the PR.” I can trust Claude to understand the context of the fix and generally get it right, where Codex can skip files, put stuff in weird places, etc.

Both of these releases feel like the companies pushing for capabilities and speed of execution in the models, but at the cost of some ease of use. I’ve found both Opus 4.6 and Codex 5.3 ignoring an instruction if I queue up multiple things to do — they’re really best when given well-scoped, clear problems (especially Codex). Claude Code’s harness has a terrible bug that makes subagents brick the terminal, where new messages say you must compact or clear, but compaction fails. 

Despite the massive step by Codex, they still have a large gap to close to Claude on the product side. Opus 4.6 is another step in the right direction, where Claude Code feels like a great experience. It’s approachable, it tends to work in the wide range of tasks I throw at it, and this’ll help them gain much broader adoption than Codex. If I’m going to recommend a coding agent to an audience who has limited-to-no software experience, it’s certainly going to be Claude. At a time when agents are just emerging into general use, this is a massive advantage, both in mindshare and feedback in terms of usage data.[1](#footnote-1)

In the meantime, there’s no cut-and-dried guideline on which agent you need to use for any use-case, you need to [use multiple models](https://www.interconnects.ai/p/use-multiple-models) all the time and keep up with the skill that is managing agents. 

Interconnects AI is a reader-supported publication. Consider becoming a subscriber.

Assessing models in 2026

There have been many hints through 2025 that we were heading toward an AI world where benchmarks associated with model releases no longer convey meaningful signal to users. Back in the time of the GPT-4 or Gemini 2.5 Pro releases, the benchmark deltas could be easily felt within the chatbot form factor of the day — models were more reliable, could do more tasks, etc. This continued through models like OpenAI’s o3. During this phase of AI’s buildout, roughly from 2023 to 2025, we were assembling the core functionality of modern language models: tool-use, extended reasoning, basic scaling, etc. The gains were obvious.

It should be clear with the releases of both Opus 4.6 and Codex 5.3 that benchmark-based release reactions barely matter. For this release, I barely looked at the evaluation scores. I saw that Opus 4.6 had a bit better search scores and Codex 5.3 used far fewer tokens per answer, but neither of these were going to make me sure they were much better models. 

Each of the AI laboratories, and the media ecosystems covering them, have been on this transition away from standard evaluations at their own pace. The most telling example is the Gemini 3 Pro release in November of 2025. The collective vibe was Google is back in the lead. Kevin Roose, self-proclaimed “[AGI-pilled](https://x.com/kevinroose/status/1900535165874827379)” NYTimes reporter in SF [said](https://www.infoq.com/news/2025/11/google-gemini-3/):

There's sort of this feeling that Google, which kind of struggled in AI for a couple of years there — they had the launch of Bard and the first versions of Gemini, which had some issues — and I think they were seen as sort of catching up to the state of the art. And now the question is: **is this them taking their crown back?**

We don’t need to dwell on the depths of Gemini’s current crisis, but they have effectively no impact at the frontier of coding agents, which as an area feels the most likely for dramatic strides in performance — dare I say, even many commonly accepted definitions of AGI that center around the notion of a “remote worker?” The timeline has left them behind 2 months after their coronation, showing Gemini 3 was hailed as a false king.

On the other end of the spectrum is Anthropic. With Anthropic’s release of Claude 4 in May of 2025, I was [skeptical of their bet on code](https://www.interconnects.ai/p/claude-4-and-anthropics-bet-on-code) — I was distracted by the glitz of OpenAI and Gemini trading blows with announcements like models achieving [IMO Gold medals](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) in mathematics or other evaluation breakthroughs.

Anthropic deserves serious credit for the focus of its vision. They were likely not the only AI lab to note the coming role of agents, but they were by far the first to shift their messaging and prioritization towards this. In my [post in June of 2025](https://www.interconnects.ai/p/summertime-outlook-o3s-novelty-coming), a month after Claude 4 was released, I was coming around to them being right to deprioritize standard benchmarks:

This is a different path for the industry and will take a different form of messaging than we’re used to. More releases are going to look like [Anthropic’s Claude 4](https://www.interconnects.ai/p/claude-4-and-anthropics-bet-on-code), where the benchmark gains are minor and the real world gains are a big step. There are plenty of more implications for policy, evaluation, and transparency that come with this. It is going to take much more nuance to understand if the pace of progress is continuing, especially as critics of AI are going to seize the opportunity of evaluations flatlining to say that AI is no longer working.

This leaves me reflecting on the role of Interconnects’ model reviews in 2026. 2025 was characterized by many dramatic, day-of model release blog posts, with the entry of many new Chinese open model builders, OpenAI’s first open language model since GPT-2, and of course the infinitely hyped GPT-5. These timely release posts still have great value — they center the conversation around the current snapshot of a company vis-a-vis the broader industry, but if models remain similar, they’ll do little to disentangle the complexity in mapping the current frontier of AI. 

In order to serve my role as an independent voice tracking the frontier models, I need to keep providing regular updates on how I’m using models, why, and why not. Over time, the industry is going to develop better ways of articulating the differences in agentic models. For the next few months, maybe even years, I expect the pace of progress to be so fast and uneven in agentic capabilities, that consistent testing and clear articulation will be the only way to monitor it.

[1](#footnote-anchor-1)

The emerging frontier of coding agents is in the use of subagents (or “[agent teams](https://code.claude.com/docs/en/agent-teams)”, which are subagents that can work together), where the primary orchestration agent sends off copies of itself to work on pieces of the problem. Claude is slightly ahead here with more polished features, but the space will evolve quickly, and maybe OpenAI can take their experiences with products like GPT-Pro to make a Pro agent.

The GPT-Pro line of models is a major advantage OpenAI has over Anthropic. I use them all the time. As we learn to use these agents for more complex, long-term tasks, harnessing more compute on a single problem will be a crucial differentiator.
