import pytest
import asyncio
from fastapi.testclient import TestClient
from athena.api.main import app
from athena.reference_run import run_reference_scenario

client = TestClient(app)

@pytest.mark.asyncio
async def test_full_athena_consulting_loop():
    """
    System-level test verifying the complete integration of core engines.
    Initially runs the reference scenario directly as a system smoke test.
    """
    # 1. Check API Health
    response = client.get("/health")
    assert response.status_code == 200

    # 2. Execute Reference Consulting Scenario
    # This scenario exercises Agent, Debate, Consensus, Document, and Diagram engines.
    try:
        await run_reference_scenario()
        scenario_success = True
    except Exception as e:
        scenario_success = False
        print(f"Scenario failed: {e}")

    assert scenario_success is True

def test_api_status_consistency():
    """
    Verify the system status API reports operational status.
    """
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "workflow" in data["engines"]
