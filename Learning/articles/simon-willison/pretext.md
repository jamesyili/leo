# Pretext

**Source:** https://simonwillison.net/2026/Mar/29/pretext/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**[Pretext](https://github.com/chenglou/pretext)**

Exciting new browser library from Cheng Lou, previously a React core developer and the original creator of the [react-motion](https://github.com/chenglou/react-motion) animation library.

Pretext solves the problem of calculating the height of a paragraph of line-wrapped text *without touching the DOM*. The usual way of doing this is to render the text and measure its dimensions, but this is extremely expensive. Pretext uses an array of clever tricks to make this much, much faster, which enables all sorts of new text rendering effects in browser applications.

Here's [one demo](https://chenglou.me/pretext/dynamic-layout/) that shows the kind of things this makes possible:

  

The key to how this works is the way it separates calculations into a call to a `prepare()` function followed by multiple calls to `layout()`.

The `prepare()` function splits the input text into segments (effectively words, but it can take things like soft hyphens and non-latin character sequences and emoji into account as well) and measures those using an off-screen canvas, then caches the results. This is comparatively expensive but only runs once.

The `layout()` function can then emulate the word-wrapping logic in browsers to figure out how many wrapped lines the text will occupy at a specified width and measure the overall height.

I [had Claude](https://claude.ai/share/7859cbe1-1350-4341-bb40-6aa241d6a1fe) build me [this interactive artifact](https://tools.simonwillison.net/pretext-explainer) to help me visually understand what's going on, based on a simplified version of Pretext itself.

The way this is tested is particularly impressive. The earlier tests [rendered a full copy of the Great Gatsby](https://github.com/chenglou/pretext/commit/d07dd7a5008726f99a15cebe0abd9031022e28ef#diff-835c37ed3b9234ed4d90c7703addb8e47f4fee6d9a28481314afd15ac472f8d2) in multiple browsers to confirm that the estimated measurements were correct against a large volume of text. This was later joined by [the corpora/ folder](https://github.com/chenglou/pretext/tree/main/corpora) using the same technique against lengthy public domain documents in Thai, Chinese, Korean, Japanese, Arabic, and more.

Cheng Lou [says](https://twitter.com/_chenglou/status/2037715226838343871):

The engine’s tiny (few kbs), aware of browser quirks, supports all the languages you’ll need, including Korean mixed with RTL Arabic and platform-specific emojis

This was achieved through showing Claude Code and Codex the browsers ground truth, and have them measure & iterate against those at every significant container width, running over weeks

    
Via [@_chenglou](https://twitter.com/_chenglou/status/2037713766205608234)

    
Tags: [browsers](https://simonwillison.net/tags/browsers), [css](https://simonwillison.net/tags/css), [javascript](https://simonwillison.net/tags/javascript), [testing](https://simonwillison.net/tags/testing), [react](https://simonwillison.net/tags/react), [typescript](https://simonwillison.net/tags/typescript)
