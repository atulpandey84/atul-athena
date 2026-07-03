import logging
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class DebateStatus(str, Enum):
    INITIAL_PROPOSAL = "initial_proposal"
    CHALLENGE_ROUND = "challenge_round"
    DEFENSE_ROUND = "defense_round"
    CONCLUDED = "concluded"
    FAILED = "failed"

class Recommendation(BaseModel):
    title: str
    pros: List[str]
    cons: List[str]
    alternatives: List[str]
    tradeoffs: List[str]
    risk: str
    cost: str
    operational_impact: str
    security_impact: str
    migration_impact: str
    final_recommendation: str

class DebateRound(BaseModel):
    round_number: int
    agent_id: str
    action: str  # e.g., "propose", "challenge", "defend"
    content: str

class DebateSession(BaseModel):
    session_id: str
    proposal_title: str
    status: DebateStatus = DebateStatus.INITIAL_PROPOSAL
    rounds: List[DebateRound] = []
    final_recommendation: Optional[Recommendation] = None

class DebateEngine:
    """
    Orchestrates architectural debates between specialist agents.
    """
    def __init__(self, max_rounds: int = 4):
        self.max_rounds = max_rounds
        self._active_sessions: Dict[str, DebateSession] = {}

    async def start_debate(self, session_id: str, title: str, proposer_id: str, proposal_content: str):
        """Initialize a new debate session."""
        session = DebateSession(session_id=session_id, proposal_title=title)
        initial_round = DebateRound(
            round_number=1,
            agent_id=proposer_id,
            action="propose",
            content=proposal_content
        )
        session.rounds.append(initial_round)
        session.status = DebateStatus.CHALLENGE_ROUND
        self._active_sessions[session_id] = session
        logger.info(f"Started debate session {session_id}: {title}")
        return session

    async def add_challenge(self, session_id: str, agent_id: str, challenge_content: str):
        """Add a challenge from a peer agent."""
        session = self._active_sessions.get(session_id)
        if not session or session.status != DebateStatus.CHALLENGE_ROUND:
            raise ValueError(f"Invalid session or state for challenge: {session_id}")

        round_num = len(session.rounds) + 1
        challenge = DebateRound(
            round_number=round_num,
            agent_id=agent_id,
            action="challenge",
            content=challenge_content
        )
        session.rounds.append(challenge)
        session.status = DebateStatus.DEFENSE_ROUND
        logger.info(f"Challenge added to session {session_id} by {agent_id}")
        return session

    async def conclude_debate(self, session_id: str, recommendation: Recommendation):
        """Conclude the debate with a final structured recommendation."""
        session = self._active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        session.final_recommendation = recommendation
        session.status = DebateStatus.CONCLUDED
        logger.info(f"Debate session {session_id} concluded")
        return session
