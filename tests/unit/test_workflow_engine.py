import pytest
import asyncio
from athena.core.workflow import WorkflowEngine, WorkflowDefinition, WorkflowStage, WorkflowStatus, StageStatus

@pytest.mark.asyncio
async def test_linear_workflow_execution():
    engine = WorkflowEngine()

    stages = [
        WorkflowStage(id="s1", name="Analysis"),
        WorkflowStage(id="s2", name="Design", dependencies=["s1"]),
        WorkflowStage(id="s3", name="Report", dependencies=["s2"])
    ]

    workflow = WorkflowDefinition(project_id="test-p", stages=stages)
    await engine.start_workflow(workflow)

    assert workflow.status == WorkflowStatus.COMPLETED
    assert all(s.status == StageStatus.COMPLETED for s in workflow.stages)

@pytest.mark.asyncio
async def test_parallel_workflow_execution():
    engine = WorkflowEngine()

    # s1 -> (s2a, s2b) -> s3
    stages = [
        WorkflowStage(id="s1", name="Init"),
        WorkflowStage(id="s2a", name="Parallel A", dependencies=["s1"]),
        WorkflowStage(id="s2b", name="Parallel B", dependencies=["s1"]),
        WorkflowStage(id="s3", name="Final", dependencies=["s2a", "s2b"])
    ]

    workflow = WorkflowDefinition(project_id="parallel-p", stages=stages)
    await engine.start_workflow(workflow)

    assert workflow.status == WorkflowStatus.COMPLETED
    assert all(s.status == StageStatus.COMPLETED for s in workflow.stages)

@pytest.mark.asyncio
async def test_workflow_failure():
    engine = WorkflowEngine()

    # Mock a failing stage by giving it an invalid ID for dependencies
    stages = [
        WorkflowStage(id="s1", name="Failer"),
    ]

    workflow = WorkflowDefinition(project_id="fail-p", stages=stages)

    # Override execute_stage to fail
    async def failing_execute(wf, stage):
        stage.status = StageStatus.FAILED
        wf.status = WorkflowStatus.FAILED

    engine._execute_stage = failing_execute

    await engine.start_workflow(workflow)
    assert workflow.status == WorkflowStatus.FAILED
    assert workflow.stages[0].status == StageStatus.FAILED
