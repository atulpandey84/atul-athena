import logging
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .debate import Recommendation, DebateSession

logger = logging.getLogger(__name__)

class ConsensusStatus(str, Enum):
    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    NEED_REVISION = "need_revision"

class ConsensusReport(BaseModel):
    session_id: str
    status: ConsensusStatus
    rationale: str
    decision_maker_id: str
    final_recommendation: Optional[Recommendation] = None

class ConsensusEngine:
    """
    Evaluates debate results and reaches a final architectural decision.
    """
    def __init__(self):
        self._reports: Dict[str, ConsensusReport] = {}

    async def evaluate_debate(self, session: DebateSession, decision_maker_id: str) -> ConsensusReport:
        """
        Evaluate a debate session and produce a consensus report.
        Initial implementation uses a basic logic: if a final recommendation exists, approve it.
        """
        logger.info(f"Evaluating consensus for session {session.session_id}")

        if not session.final_recommendation:
            status = ConsensusStatus.ESCALATED
            rationale = "No final recommendation reached during debate."
        else:
            # Placeholder for more complex evaluation logic
            status = ConsensusStatus.APPROVED
            rationale = f"Consensus reached based on final recommendation: {session.final_recommendation.title}"

        report = ConsensusReport(
            session_id=session.session_id,
            status=status,
            rationale=rationale,
            decision_maker_id=decision_maker_id,
            final_recommendation=session.final_recommendation
        )

        self._reports[session.session_id] = report
        return report

    async def get_report(self, session_id: str) -> Optional[ConsensusReport]:
        """Retrieve a previous consensus report."""
        return self._reports.get(session_id)
