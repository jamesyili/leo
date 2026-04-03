# datasette-files 0.1a3

**Source:** https://simonwillison.net/2026/Mar/30/datasette-files/#atom-everything
**Ingested:** 2026-04-02
**Tags:** llm-tooling, ai-engineering

---

**Release:** [datasette-files 0.1a3](https://github.com/datasette/datasette-files/releases/tag/0.1a3)

    
I'm working on integrating `datasette-files` into other plugins, such as [datasette-extract](https://github.com/datasette/datasette-extract). This necessitated a new release of the base plugin.

`owners_can_edit` and `owners_can_delete` configuration options, plus the `files-edit` and `files-delete` actions are now scoped to a new `FileResource` which is a child of `FileSourceResource`. [#18](https://github.com/datasette/datasette-files/issues/18)

The file picker UI is now available as a `<datasette-file-picker>` Web Component. Thanks, [Alex Garcia](https://github.com/asg017). [#19](https://github.com/datasette/datasette-files/issues/19)

New `from datasette_files import get_file` Python API for other plugins that need to access file data. [#20](https://github.com/datasette/datasette-files/issues/20)

    
        
Tags: [datasette](https://simonwillison.net/tags/datasette)
