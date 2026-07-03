# ADR 0010: Workflow Engine Design

## Status
Accepted

## Context
ATHENA needs to orchestrate complex, multi-agent consulting processes that span multiple stages, involve peer review, and require high reliability.

## Decision
We will implement the Workflow Engine based on an event-driven and state-machine pattern:
1.  **DAG-based Workflows**: Support defining workflows as Directed Acyclic Graphs of stages to handle complex dependencies.
2.  **Async/Event-Driven**: Stage transitions will be triggered by events (e.g., `TaskCompleted`, `ReviewApproved`).
3.  **Stateful Persistence**: The engine will track and persist the state of each workflow and its stages using a centralized state manager.
4.  **Decoupled Execution**: The engine orchestrates *when* tasks happen, while the Agent Framework handles *how* they are executed.

## Consequences
- Enables complex, industrial-grade consulting processes.
- Improved observability of the consulting lifecycle.
- Facilitates re-entrancy and recovery for long-running projects.
- Increased complexity in the core framework to manage cross-component events and state synchronization.
