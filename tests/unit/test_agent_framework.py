import pytest
import asyncio
from athena.core.agent import BaseAgent
from athena.core.models import AgentRole, AgentState, AgentMessage

class MockAgent(BaseAgent):
    async def execute_task(self, task):
        await self.transition_to(AgentState.ACTING)
        return {"result": "success"}

@pytest.mark.asyncio
async def test_agent_initialization():
    role = AgentRole(
        name="Test Architect",
        responsibilities=["Testing stuff"],
        goals=["Pass tests"]
    )
    agent = MockAgent(agent_id="test-001", role=role)

    assert agent.agent_id == "test-001"
    assert agent.role.name == "Test Architect"
    assert agent.state == AgentState.IDLE

    await agent.initialize()
    assert agent.state == AgentState.IDLE

@pytest.mark.asyncio
async def test_agent_state_transition():
    role = AgentRole(name="Test", responsibilities=[], goals=[])
    agent = MockAgent(agent_id="test-002", role=role)

    await agent.transition_to(AgentState.THINKING)
    assert agent.state == AgentState.THINKING

    result = await agent.execute_task({})
    assert result["result"] == "success"
    assert agent.state == AgentState.ACTING

@pytest.mark.asyncio
async def test_agent_communication():
    role = AgentRole(name="Test", responsibilities=[], goals=[])
    agent_a = MockAgent(agent_id="agent-a", role=role)
    agent_b = MockAgent(agent_id="agent-b", role=role)

    message = await agent_a.send_message(
        receiver_id="agent-b",
        content={"data": "hello"},
        message_type="test_msg"
    )

    assert message.sender_id == "agent-a"
    assert message.receiver_id == "agent-b"
    assert message.content["data"] == "hello"

    await agent_b.receive_message(message)
    assert agent_b._message_queue.qsize() == 1

    # Test handling messages
    task = asyncio.create_task(agent_b.handle_messages())
    await asyncio.sleep(0.1)
    assert agent_b._message_queue.qsize() == 0
    task.cancel()
