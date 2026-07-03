# ADR 0016: Tool Framework Design

## Status
Accepted

## Context
Agents need a secure and extensible way to interact with infrastructure tools and APIs. A monolithic toolset is difficult to maintain and lacks the flexibility required for an enterprise consulting platform.

## Decision
We will implement a plugin-based Tool Framework:
1.  **BaseTool Abstraction**: All tools will inherit from a common `BaseTool` class that enforces an asynchronous `run()` interface.
2.  **Pydantic Schema Validation**: Every tool will define its input requirements using a Pydantic model, ensuring that agents provide valid data before execution.
3.  **Discovery via ToolManager**: A centralized `ToolManager` will handle tool registration, lifecycle, and access control.
4.  **Subprocess Isolation**: For CLI-based tools (Terraform, AWS CLI), the framework will use `asyncio.create_subprocess_exec` to ensure non-blocking execution and output capture.
5.  **MCP Readiness**: The framework will be designed to wrap and expose MCP servers as ATHENA-native tools.

## Consequences
- Highly modular system where new capabilities can be added as standalone plugins.
- Improved reliability through strict input validation.
- Secure execution environment with captured audit logs.
- Requires careful handling of environment variables and secrets during tool execution.
