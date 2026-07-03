import pytest
import os
import asyncio
from athena.core.document import DocumentEngine
from athena.core.consensus import ConsensusReport, ConsensusStatus
from athena.core.debate import Recommendation

@pytest.mark.asyncio
async def test_markdown_report_generation(tmp_path):
    # Use tmp_path for output
    engine = DocumentEngine(output_dir=str(tmp_path))

    rec = Recommendation(
        title="Serverless Migration",
        pros=["Scale"], cons=["Cold start"], alternatives=["Fargate"],
        tradeoffs=["Cost/Latency"], risk="Low", cost="Low",
        operational_impact="Minimal", security_impact="Good",
        migration_impact="Med", final_recommendation="Go"
    )

    report = ConsensusReport(
        session_id="session-1",
        status=ConsensusStatus.APPROVED,
        rationale="Strong tradeoffs.",
        decision_maker_id="chief-arch",
        final_recommendation=rec
    )

    output = await engine.generate_markdown_report(report)

    assert output.format == "markdown"
    assert os.path.exists(output.content)

    with open(output.content, 'r') as f:
        content = f.read()
        assert "# Serverless Migration" in content
        assert "**Status**: APPROVED" in content
        assert "**Decision Maker**: chief-arch" in content
        assert "- Scale" in content
        assert "- Cold start" in content

@pytest.mark.asyncio
async def test_deliverable_package(tmp_path):
    engine = DocumentEngine(output_dir=str(tmp_path))
    report = ConsensusReport(
        session_id="session-2",
        status=ConsensusStatus.APPROVED,
        rationale="Ok",
        decision_maker_id="arch-1"
    )

    outputs = await engine.generate_deliverable_package(report, ["markdown"])
    assert len(outputs) == 1
    assert outputs[0].format == "markdown"
