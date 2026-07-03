# ADR 0015: Prompt Framework Design

## Status
Accepted

## Context
Managing prompts for dozens of specialized agents is complex and error-prone. We need a system that ensures consistency, reusability, and dynamic context injection while maintaining human-readability.

## Decision
We will implement the Prompt Framework using Jinja2 and a "Docs as Code" structure:
1.  **Jinja2 Templating**: Use the Jinja2 engine for all prompt rendering, allowing for variables, conditionals, and template inheritance.
2.  **Modular Composition**: Prompts will be built from reusable fragments (macros/includes) stored in `docs/prompts/common/`.
3.  **Markdown-Based Storage**: Prompts will be authored in Markdown for ease of review and versioning in Git.
4.  **Runtime Injection**: The `PromptManager` will handle injecting runtime context from the Memory and Knowledge frameworks into the templates.
5.  **Agent-Prompt Mapping**: A configuration model will map agent roles to their primary prompt templates.

## Consequences
- Highly reusable and maintainable prompt library.
- Easy testing and iteration of prompt changes.
- Ensures all agents follow the same core "guardrails" and formatting rules.
- Adds a dependency on the Jinja2 library.
