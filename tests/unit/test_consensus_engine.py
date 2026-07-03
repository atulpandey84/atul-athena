import pytest
import asyncio
from athena.core.consensus import ConsensusEngine, ConsensusStatus
from athena.core.debate import DebateSession, Recommendation

@pytest.mark.asyncio
async def test_consensus_approval():
    engine = ConsensusEngine()

    rec = Recommendation(
        title="Test Design",
        pros=[], cons=[], alternatives=[], tradeoffs=[],
        risk="Low", cost="Low", operational_impact="None",
        security_impact="None", migration_impact="None",
        final_recommendation="Go"
    )

    session = DebateSession(
        session_id="deb-123",
        proposal_title="Test Design",
        final_recommendation=rec
    )

    report = await engine.evaluate_debate(session, "chief-arch")
    assert report.status == ConsensusStatus.APPROVED
    assert report.session_id == "deb-123"
    assert report.decision_maker_id == "chief-arch"
    assert report.final_recommendation.title == "Test Design"

@pytest.mark.asyncio
async def test_consensus_escalation():
    engine = ConsensusEngine()

    # Session without final recommendation
    session = DebateSession(
        session_id="deb-failed",
        proposal_title="Risky Design"
    )

    report = await engine.evaluate_debate(session, "chief-arch")
    assert report.status == ConsensusStatus.ESCALATED
    assert "No final recommendation" in report.rationale
