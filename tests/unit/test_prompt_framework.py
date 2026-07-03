import pytest
import os
import asyncio
from athena.core.prompt import PromptManager

@pytest.mark.asyncio
async def test_prompt_rendering(tmp_path):
    # Setup temporary prompt base
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "common").mkdir()
    (prompt_dir / "agents").mkdir()

    persona_file = prompt_dir / "common" / "persona.md"
    persona_file.write_text("Role: {{ role_name }}")

    agent_file = prompt_dir / "agents" / "tester.md"
    agent_file.write_text("{% include 'common/persona.md' %}\nTask: {{ task }}")

    manager = PromptManager(prompt_base_path=str(prompt_dir))

    rendered = await manager.render_agent_prompt(
        agent_role="tester",
        context={"role_name": "QA Bot", "task": "Verify code"}
    )

    assert "Role: QA Bot" in rendered
    assert "Task: Verify code" in rendered

@pytest.mark.asyncio
async def test_prompt_missing_template():
    manager = PromptManager()
    with pytest.raises(Exception):
        await manager.render_agent_prompt("non-existent", {})
