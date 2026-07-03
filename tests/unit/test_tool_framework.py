import pytest
import asyncio
from pydantic import BaseModel, Field
from athena.core.tool import BaseTool, ToolManager, ToolResult

class MockInput(BaseModel):
    command: str
    target: str = "default"

class MockTool(BaseTool):
    async def run(self, **kwargs) -> ToolResult:
        inputs = self.validate_input(**kwargs)
        return ToolResult(
            tool_name=self.name,
            success=True,
            output=f"Executed {inputs.command} on {inputs.target}",
            return_code=0
        )

@pytest.mark.asyncio
async def test_tool_registration_and_execution():
    manager = ToolManager()
    tool = MockTool(
        name="test-tool",
        description="A mock tool for testing",
        input_model=MockInput
    )

    manager.register_tool(tool)

    # Discovery
    registered = manager.get_tool("test-tool")
    assert registered is not None
    assert registered.name == "test-tool"

    # Execution
    result = await manager.execute_tool("test-tool", command="ping", target="host1")
    assert result.success is True
    assert "Executed ping on host1" in result.output

@pytest.mark.asyncio
async def test_tool_input_validation():
    manager = ToolManager()
    tool = MockTool(name="val-tool", description="X", input_model=MockInput)
    manager.register_tool(tool)

    # Missing required field 'command'
    with pytest.raises(Exception):
        await manager.execute_tool("val-tool", target="nothing")

@pytest.mark.asyncio
async def test_tool_not_found():
    manager = ToolManager()
    with pytest.raises(ValueError, match="Tool not found"):
        await manager.execute_tool("ghost", cmd="x")
