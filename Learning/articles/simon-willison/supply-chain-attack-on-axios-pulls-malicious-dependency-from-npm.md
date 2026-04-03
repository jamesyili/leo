# Supply Chain Attack on Axios Pulls Malicious Dependency from npm

**Source:** https://simonwillison.net/2026/Mar/31/supply-chain-attack-on-axios/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**[Supply Chain Attack on Axios Pulls Malicious Dependency from npm](https://socket.dev/blog/axios-npm-package-compromised)**

Useful writeup of today's supply chain attack against Axios, the HTTP client NPM package with [101 million weekly downloads](https://www.npmjs.com/package/axios). Versions `1.14.1` and `0.30.4` both included a new dependency called `plain-crypto-js` which was freshly published malware, stealing credentials and installing a remote access trojan (RAT).

It looks like the attack came from a leaked long-lived npm token. Axios have [an open issue to adopt trusted publishing](https://github.com/axios/axios/issues/7055), which would ensure that only their GitHub Actions workflows are able to publish to npm. The malware packages were published without an accompanying GitHub release, which strikes me as a useful heuristic for spotting potentially malicious releases - the same pattern was present for LiteLLM [last week](https://simonwillison.net/2026/Mar/24/malicious-litellm/) as well.

    
Via [lobste.rs](https://lobste.rs/s/l57wuc/supply_chain_attack_on_axios)

    
Tags: [javascript](https://simonwillison.net/tags/javascript), [security](https://simonwillison.net/tags/security), [npm](https://simonwillison.net/tags/npm), [supply-chain](https://simonwillison.net/tags/supply-chain)
