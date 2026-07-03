import abc
import asyncio
import logging
import time
from typing import Optional, List, Dict, Any
from .models import AgentState, AgentRole, AgentMessage

logger = logging.getLogger(__name__)

class BaseAgent(abc.ABC):
    """
    Base class for all ATHENA agents.
    """
    def __init__(self, agent_id: str, role: AgentRole):
        self.agent_id = agent_id
        self.role = role
        self.state = AgentState.IDLE
        self.memory: Dict[str, Any] = {}
        self.tools: List[Any] = []
        self._message_queue: asyncio.Queue = asyncio.Queue()

    async def initialize(self):
        """Initialize the agent and its components."""
        logger.info(f"Initializing agent {self.agent_id} ({self.role.name})")
        await self.transition_to(AgentState.IDLE)

    @abc.abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task."""
        pass

    async def transition_to(self, new_state: AgentState):
        """Manage agent state transitions."""
        logger.debug(f"Agent {self.agent_id} transitioning: {self.state} -> {new_state}")
        self.state = new_state

    async def send_message(self, receiver_id: str, content: Dict[str, Any], message_type: str):
        """Construct and send a message."""
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            content=content,
            message_type=message_type,
            timestamp=time.time()
        )
        logger.info(f"Agent {self.agent_id} sending {message_type} to {receiver_id}")
        return message

    async def receive_message(self, message: AgentMessage):
        """Process an incoming message."""
        logger.info(f"Agent {self.agent_id} received {message.message_type} from {message.sender_id}")
        await self._message_queue.put(message)

    async def handle_messages(self):
        """Listen for and process messages in the queue."""
        while True:
            message = await self._message_queue.get()
            # Basic message handling logic
            logger.debug(f"Agent {self.agent_id} processing message: {message.message_type}")
            self._message_queue.task_done()
