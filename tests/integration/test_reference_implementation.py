import pytest
import os
import asyncio
from athena.reference_run import run_reference_scenario

@pytest.mark.asyncio
async def test_reference_scenario_execution():
    # Ensure output directory exists or is handled by script
    output_path = "docs/examples/reference_output/report_deb-ref-001.md"
    if os.path.exists(output_path):
        os.remove(output_path)

    await run_reference_scenario()

    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        content = f.read()
        assert "# Serverless Migration Strategy" in content
        assert "## Architecture Diagram" in content
        assert "graph TD" in content
        assert "Lambda" in content
