import abc
import asyncio
import logging
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ToolResult(BaseModel):
    tool_name: str
    success: bool
    output: str
    error: Optional[str] = None
    return_code: Optional[int] = None

class BaseTool(abc.ABC):
    """
    Abstract base class for all ATHENA tools.
    """
    def __init__(self, name: str, description: str, input_model: Type[BaseModel]):
        self.name = name
        self.description = description
        self.input_model = input_model

    @abc.abstractmethod
    async def run(self, **kwargs) -> ToolResult:
        """Execute the tool logic."""
        pass

    def validate_input(self, **kwargs) -> BaseModel:
        """Validate input arguments against the defined Pydantic model."""
        return self.input_model(**kwargs)

class ToolManager:
    """
    Manages registration, discovery, and execution of tools.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """Register a new tool instance."""
        self._tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        """List all registered tools."""
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

    async def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """Helper to find and execute a tool."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")

        # Validate before execution
        tool.validate_input(**kwargs)

        logger.info(f"Executing tool: {name}")
        return await tool.run(**kwargs)
