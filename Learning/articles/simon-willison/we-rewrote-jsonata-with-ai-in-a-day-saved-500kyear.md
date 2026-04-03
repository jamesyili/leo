# We Rewrote JSONata with AI in a Day, Saved $500K/Year

**Source:** https://simonwillison.net/2026/Mar/27/vine-porting-jsonata/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**[We Rewrote JSONata with AI in a Day, Saved $500K/Year](https://www.reco.ai/blog/we-rewrote-jsonata-with-ai)**

Bit of a hyperbolic framing but this looks like another case study of **vibe porting**, this time spinning up a new custom Go implementation of the [JSONata](https://jsonata.org) JSON expression language - similar in focus to jq, and heavily associated with the [Node-RED](https://nodered.org) platform.

As with other vibe-porting projects the key enabling factor was JSONata's existing test suite, which helped build the first working Go version in 7 hours and $400 of token spend.

The Reco team then used a shadow deployment for a week to run the new and old versions in parallel to confirm the new implementation exactly matched the behavior of the old one.

    
Tags: [go](https://simonwillison.net/tags/go), [json](https://simonwillison.net/tags/json), [ai](https://simonwillison.net/tags/ai), [generative-ai](https://simonwillison.net/tags/generative-ai), [llms](https://simonwillison.net/tags/llms), [agentic-engineering](https://simonwillison.net/tags/agentic-engineering), [vibe-porting](https://simonwillison.net/tags/vibe-porting)
