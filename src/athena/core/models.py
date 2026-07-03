from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AgentState(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    COMMUNICATING = "communicating"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentRole(BaseModel):
    name: str
    responsibilities: List[str]
    goals: List[str]

class AgentMessage(BaseModel):
    sender_id: str
    receiver_id: str
    content: Dict[str, Any]
    message_type: str
    timestamp: float
