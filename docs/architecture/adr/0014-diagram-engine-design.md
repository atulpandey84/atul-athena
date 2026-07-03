# ADR 0014: Diagram Engine Design

## Status
Accepted

## Context
Architectural recommendations are more effective when accompanied by clear diagrams. Manual creation by agents is inconsistent and prone to errors. We need a programmatic approach.

## Decision
We will implement the Diagram Engine using a "DSL-first" approach:
1.  **Diagram-as-Code (DaC)**: All diagrams will be represented internally as structured data models and output as standard DSLs (primarily Mermaid and PlantUML).
2.  **Internal Model Mapping**: We will define a set of high-level models (e.g., `ArchitectureNode`, `Connection`, `Interaction`) that the engine translates into specific DSL syntax.
3.  **Mermaid as Primary Output**: Mermaid will be the default for documentation and reports due to its native support in MkDocs and many enterprise tools.
4.  **Provider-Based Architecture**: Different generators (Mermaid, PlantUML, D2) will be implemented as pluggable providers to allow for easy extension.

## Consequences
- Consistent and high-quality visual deliverables.
- Diagrams are stored as source code, making them easy to version and diff.
- Reduced "hallucination" in agent-produced visuals by enforcing strict syntax rules through the engine.
- Requires mapping between abstract architectural concepts and specific visual primitives of the DSLs.
