import logging
import time
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class MemoryTier(str, Enum):
    CONVERSATION = "conversation"
    WORKING = "working"
    SEMANTIC = "semantic"
    LONG_TERM = "long_term"
    ORGANIZATIONAL = "organizational"

class MemoryEntry(BaseModel):
    tier: MemoryTier
    scope_id: str  # Can be agent_id, project_id, etc.
    content: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = {}

class MemoryManager:
    """
    Manages multi-tiered memory storage and retrieval for ATHENA agents.
    """
    def __init__(self):
        self._storage: Dict[MemoryTier, Dict[str, List[MemoryEntry]]] = {
            tier: {} for tier in MemoryTier
        }

    async def store(self, tier: MemoryTier, scope_id: str, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        """Store an entry in a specific memory tier and scope."""
        entry = MemoryEntry(
            tier=tier,
            scope_id=scope_id,
            content=content,
            metadata=metadata or {}
        )

        if scope_id not in self._storage[tier]:
            self._storage[tier][scope_id] = []

        self._storage[tier][scope_id].append(entry)
        logger.debug(f"Stored {tier} memory for {scope_id}")

    async def retrieve(self, tier: MemoryTier, scope_id: str, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve the most recent entries from a specific tier and scope."""
        entries = self._storage[tier].get(scope_id, [])
        return sorted(entries, key=lambda x: x.timestamp, reverse=True)[:limit]

    async def search_working_memory(self, scope_id: str, key: str, value: Any) -> List[MemoryEntry]:
        """Search working memory by metadata or content key-value pair."""
        entries = self._storage[MemoryTier.WORKING].get(scope_id, [])
        results = []
        for e in entries:
            if e.content.get(key) == value or e.metadata.get(key) == value:
                results.append(e)
        return results

    async def clear_scope(self, tier: MemoryTier, scope_id: str):
        """Clear memory for a specific tier and scope."""
        if scope_id in self._storage[tier]:
            del self._storage[tier][scope_id]
            logger.info(f"Cleared {tier} memory for {scope_id}")
