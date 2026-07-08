# ADR 0020: Testing Strategy

## Status
Accepted

## Context
Ensuring the reliability and quality of an autonomous consulting organization requires more than just unit tests. We need a strategy that covers agent behavior, multi-framework integration, and the quality of final deliverables.

## Decision
We will adopt a multi-layered testing strategy:
1.  **Unit Tests**: Focused on the core logic of individual engines (Agent, Memory, Tool, etc.) using `pytest`.
2.  **Integration Tests**: Focused on the orchestration between engines (Workflow + Agent, Debate + Consensus) and the end-to-end reference implementation.
3.  **System Tests**: Focused on exercising the platform via the API boundary using `TestClient` to ensure external interfaces work as expected.
4.  **Mocked Externals**: All external LLM and Tool calls will be mocked in the primary test suites to ensure speed, cost-efficiency, and determinism.
5.  **Deliverable Validation**: Automated checks for the syntax and structure of generated Markdown and Mermaid assets.

## Consequences
- High confidence in the reliability of the platform's core frameworks.
- Easier discovery of integration issues between distributed components.
- Standardized way for developers and AI agents to verify their contributions.
- Increased development time to maintain a comprehensive test suite.
