# Distilled • Google Docs

**Source:** https://aman.ai/sysdes/google-docs/
**Ingested:** 2026-04-02
**Tags:** system-design

---

design further readingdesign clients send document editing operations to the websocket server the real time communication is handled by the websocket server documents operations are persisted in the message queue the file operation server consumes operations produced by clients and generates transformed operations using collaboration algorithms three types of data are stored file metadata file content and operations one of the biggest challenges is real time conflict resolution common algorithms include operational transformation ot differential synchronization ds conflict free replicated data type crdt google doc uses ot according to its wikipedia page and crdt is an active area of research for real time concurrent editing further reading powered by ai instagram s explore recommender system how to design google docs episode 4
