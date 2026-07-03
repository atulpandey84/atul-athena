import asyncio
import logging
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    HALTED = "halted"

class StageStatus(str, Enum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_FOR_REVIEW = "waiting_for_review"

class WorkflowStage(BaseModel):
    id: str
    name: str
    dependencies: List[str] = []
    status: StageStatus = StageStatus.READY
    task_config: Dict[str, Any] = {}
    result: Optional[Dict[str, Any]] = None

class WorkflowDefinition(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    stages: List[WorkflowStage]
    status: WorkflowStatus = WorkflowStatus.PENDING

class WorkflowEngine:
    """
    Orchestrates the execution of ATHENA multi-agent workflows.
    """
    def __init__(self):
        self._active_workflows: Dict[str, WorkflowDefinition] = {}

    async def start_workflow(self, workflow: WorkflowDefinition):
        """Register and start a workflow."""
        workflow.status = WorkflowStatus.RUNNING
        self._active_workflows[workflow.id] = workflow
        logger.info(f"Started workflow {workflow.id} for project {workflow.project_id}")
        await self._process_workflow(workflow)

    async def _process_workflow(self, workflow: WorkflowDefinition):
        """Main processing loop for a workflow."""
        while workflow.status == WorkflowStatus.RUNNING:
            runnable_stages = self._get_runnable_stages(workflow)

            if not runnable_stages:
                if self._all_stages_completed(workflow):
                    workflow.status = WorkflowStatus.COMPLETED
                    logger.info(f"Workflow {workflow.id} completed successfully")
                else:
                    # Check for failures or halts
                    if self._has_failed_stages(workflow):
                        workflow.status = WorkflowStatus.FAILED
                    else:
                        # Waiting for external triggers or async tasks
                        break
                continue

            # Execute runnable stages (potentially in parallel)
            tasks = [self._execute_stage(workflow, stage) for stage in runnable_stages]
            await asyncio.gather(*tasks)

    def _get_runnable_stages(self, workflow: WorkflowDefinition) -> List[WorkflowStage]:
        runnable = []
        completed_stage_ids = {s.id for s in workflow.stages if s.status == StageStatus.COMPLETED}

        for stage in workflow.stages:
            if stage.status == StageStatus.READY:
                if all(dep in completed_stage_ids for dep in stage.dependencies):
                    runnable.append(stage)
        return runnable

    async def _execute_stage(self, workflow: WorkflowDefinition, stage: WorkflowStage):
        logger.info(f"Executing stage {stage.name} ({stage.id}) in workflow {workflow.id}")
        stage.status = StageStatus.IN_PROGRESS

        try:
            # Placeholder for actual stage execution logic involving Agent Framework
            await asyncio.sleep(0.1)
            stage.status = StageStatus.COMPLETED
            logger.info(f"Stage {stage.name} completed")
        except Exception as e:
            logger.error(f"Error executing stage {stage.id}: {e}")
            stage.status = StageStatus.FAILED
            workflow.status = WorkflowStatus.FAILED

    def _all_stages_completed(self, workflow: WorkflowDefinition) -> bool:
        return all(s.status == StageStatus.COMPLETED for s in workflow.stages)

    def _has_failed_stages(self, workflow: WorkflowDefinition) -> bool:
        return any(s.status == StageStatus.FAILED for s in workflow.stages)

    async def trigger_workflow_update(self, workflow_id: str):
        """Manually trigger a processing loop (e.g. after a human review)."""
        if workflow_id in self._active_workflows:
            await self._process_workflow(self._active_workflows[workflow_id])
