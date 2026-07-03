import pytest
import asyncio
from athena.core.memory import MemoryManager, MemoryTier

@pytest.mark.asyncio
async def test_memory_storage_and_retrieval():
    manager = MemoryManager()

    # Store conversation memory
    await manager.store(
        tier=MemoryTier.CONVERSATION,
        scope_id="agent-001",
        content={"msg": "Hello Agent"},
        metadata={"user": "admin"}
    )

    entries = await manager.retrieve(MemoryTier.CONVERSATION, "agent-001")
    assert len(entries) == 1
    assert entries[0].content["msg"] == "Hello Agent"
    assert entries[0].metadata["user"] == "admin"

@pytest.mark.asyncio
async def test_memory_tier_isolation():
    manager = MemoryManager()

    await manager.store(MemoryTier.WORKING, "project-a", {"task": "analysis"})
    await manager.store(MemoryTier.CONVERSATION, "project-a", {"chat": "hi"})

    working = await manager.retrieve(MemoryTier.WORKING, "project-a")
    conv = await manager.retrieve(MemoryTier.CONVERSATION, "project-a")

    assert len(working) == 1
    assert working[0].content["task"] == "analysis"
    assert len(conv) == 1
    assert conv[0].content["chat"] == "hi"

@pytest.mark.asyncio
async def test_search_working_memory():
    manager = MemoryManager()

    await manager.store(
        tier=MemoryTier.WORKING,
        scope_id="project-b",
        content={"id": "req-1", "status": "pending"}
    )
    await manager.store(
        tier=MemoryTier.WORKING,
        scope_id="project-b",
        content={"id": "req-2", "status": "completed"}
    )

    results = await manager.search_working_memory("project-b", "status", "completed")
    assert len(results) == 1
    assert results[0].content["id"] == "req-2"

@pytest.mark.asyncio
async def test_clear_memory_scope():
    manager = MemoryManager()

    await manager.store(MemoryTier.CONVERSATION, "agent-x", {"data": "..."})
    await manager.clear_scope(MemoryTier.CONVERSATION, "agent-x")

    entries = await manager.retrieve(MemoryTier.CONVERSATION, "agent-x")
    assert len(entries) == 0
