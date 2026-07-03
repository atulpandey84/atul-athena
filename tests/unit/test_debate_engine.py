import pytest
import asyncio
from athena.core.debate import DebateEngine, Recommendation, DebateStatus

@pytest.mark.asyncio
async def test_debate_workflow():
    engine = DebateEngine()
    session_id = "deb-001"

    # 1. Start Debate
    session = await engine.start_debate(
        session_id=session_id,
        title="Serverless Migration",
        proposer_id="cloud-arch",
        proposal_content="Migrate all APIs to AWS Lambda"
    )
    assert session.status == DebateStatus.CHALLENGE_ROUND
    assert len(session.rounds) == 1

    # 2. Peer Challenge
    await engine.add_challenge(
        session_id=session_id,
        agent_id="sec-arch",
        challenge_content="Lambda cold starts may impact security scanning latency"
    )
    assert session.status == DebateStatus.DEFENSE_ROUND
    assert len(session.rounds) == 2

    # 3. Conclude with Structured Recommendation
    rec = Recommendation(
        title="Serverless Migration with Provisioned Concurrency",
        pros=["Scale", "Cost"],
        cons=["Cold starts"],
        alternatives=["Fargate"],
        tradeoffs=["Latency vs Cost"],
        risk="Low",
        cost="Variable",
        operational_impact="Low",
        security_impact="Neutral",
        migration_impact="Significant",
        final_recommendation="Proceed with provisioned concurrency"
    )

    final_session = await engine.conclude_debate(session_id, rec)
    assert final_session.status == DebateStatus.CONCLUDED
    assert final_session.final_recommendation.risk == "Low"

@pytest.mark.asyncio
async def test_invalid_debate_transition():
    engine = DebateEngine()
    session_id = "deb-002"

    await engine.start_debate(session_id, "Title", "agent1", "content")

    # Try to add challenge again (should fail because it transitions to DEFENSE_ROUND)
    await engine.add_challenge(session_id, "agent2", "challenge")

    with pytest.raises(ValueError, match="Invalid session or state for challenge"):
        await engine.add_challenge(session_id, "agent3", "another challenge")
