# datasette-llm-usage 0.2a0

**Source:** https://simonwillison.net/2026/Apr/1/datasette-llm-usage/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**Release:** [datasette-llm-usage 0.2a0](https://github.com/datasette/datasette-llm-usage/releases/tag/0.2a0)

    

Removed features relating to allowances and estimated pricing. These are now the domain of [datasette-llm-accountant](https://github.com/datasette/datasette-llm-accountant).

Now depends on [datasette-llm](https://github.com/datasette/datasette-llm) for model configuration. [#3](https://github.com/datasette/datasette-llm-usage/pull/3)

Full prompts and responses and tool calls can now be logged to the `llm_usage_prompt_log` table in the internal database if you set the new `datasette-llm-usage.log_prompts` plugin configuration setting.

Redesigned the `/-/llm-usage-simple-prompt` page, which now requires the `llm-usage-simple-prompt` permission.

    
        
Tags: [llm](https://simonwillison.net/tags/llm), [datasette](https://simonwillison.net/tags/datasette)
