# Skupper — Documentation Contribution Guide

## Purpose

This guide exists to help contributors propose, submit, and review documentation changes to Skupper in a way that maintains clarity, quality, and long-term maintainability. It covers philosophy, expectations (including guidelines around AI-assisted contributions), and the workflow for submitting changes.

## Core Principles

1. **Human responsibility first**  
	Even if documentation is drafted or assisted by an LLM, the *human contributor* is fully responsible for correctness, clarity, accuracy, and completeness of the docs. The final decision always lies with a human reviewer/maintainer.
2. **Docs as code — treat it seriously**  
	Documentation is part of the project’s infrastructure. It should follow the same rigor as code: well-structured, tested (links check, formatting, linting), and reviewed thoroughly.
3. **Open and welcoming to all valid contributors**  
	Everyone — whether a core maintainer or first-time contributor — is welcome to improve docs, fix typos, update outdated instructions, or add new content (tutorials, examples, API reference, etc.) as long as they follow these guidelines.
4. **Transparency about tooling**  
	If you use AI tools (LLMs) to assist writing or editing documentation, please disclose what you used, prompts (if relevant), what required further manual editing, and any limitations or caveats discovered. This helps maintainers audit quality and refine guidelines over time.

## What Kind of Contributions Are Welcome

- Typo corrections, grammar fixes, formatting improvements
- Updating outdated content (commands, examples, version references)
- Adding missing content: new guides, tutorials, examples (e.g. new platform support, advanced use cases), missing edge-case docs, extensions to CLI/API docs
- Improving clarity: re-structure complex pages, better headings/subheadings, cross-links, glossary entries, diagrams or ASCII diagrams
- Translation (if project supports it) or multi-language documentation (depending on community interest)
- Improving doc infrastructure: adding or improving linters, link-checkers, CI tests for docs, templates for docs, consistent style conventions


## When (and How) to Use AI Assistance or Automation

Because generative AI is now widely accessible, we allow its use — but under constraints:

- You may use AI to assist with small tasks: rewording sentences, catching grammar/spelling, as a first draft of small sections, or to help with refactoring prose.
- You should *not* rely on AI to generate large doc sets from scratch (e.g. full guides, reference material, diagrams) — these require human domain knowledge and careful validation.
- Always treat AI-assisted content as a draft: you must manually review, test, and verify everything (commands, code snippets, YAML, CLI/API correctness, link validity, clarity).
- In your Pull Request (PR) description, include a short disclosure if you used AI tools. Example: tool name, what it generated, what you manually edited, limitations you found. This transparency helps maintain consistent doc quality over time.


## How to Contribute — Workflow

1. **Fork the repo and clone it**
	
2. **Familiarize yourself with the doc structure**  
	Explore existing directories (e.g. `input`, `includes`, etc.) to understand where your change logically fits. The repository layout reflects existing organization of topics such as Overview, Getting Started, CLI references.
3. **Make your changes — in Markdown**  
	Use Markdown and follow existing style conventions (code blocks, headings, link style). If adding new pages, consider updating navigation/TOC accordingly.
4. **Run docs checks / linters / link checkers**  
	Ensure your changes compile cleanly, links aren’t broken, formatting is consistent, no stray formatting issues, etc.
	```shell
	./plano test # creates html in output dir and checks links, etc
	```
5. **Commit & push your changes, then open a Pull Request (PR)**
	- Write a clear PR title: short but descriptive.
	- In the PR body: explain what changes you made and why. If you used AI assistance, include disclosure.
	- Reference related issues if applicable, or open a new issue describing the problem/need before or along with your PR.
6. **Undergo review**  
	Maintainers or other contributors will review for correctness, clarity, style, completeness. Be responsive to feedback.


## Tone & Style Expectations

- Use a clear, concise, friendly, and inclusive tone — documentation should be welcoming to all readers.
- Prefer clarity over cleverness — prioritize readability and maintainability.
- Attribute external references (links, commands, external tools) and explain *why* they are useful. Avoid gratuitous opinion or tool advocacy.

## Recognition & Encouragement

- We value all doc contributions — whether small typo fixes or large new guides.
- Maintainers will publicly acknowledge contributors 

## Summary & Your Next Step

If you care about Skupper, use it, or plan to use it — your perspective is valuable. Whether you fix a typo, clarify a confusing paragraph, add a full tutorial, or improve API reference: every improvement helps.
