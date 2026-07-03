import logging
import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

class PromptManager:
    """
    Manages loading, templating, and rendering of agent prompts.
    """
    def __init__(self, prompt_base_path: str = "docs/prompts"):
        self.prompt_base_path = prompt_base_path
        self.env = Environment(
            loader=FileSystemLoader(prompt_base_path),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

    async def render_prompt(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        Render a specific prompt template with the provided context.
        template_path should be relative to prompt_base_path.
        """
        logger.info(f"Rendering prompt template: {template_path}")
        try:
            template = self.env.get_template(template_path)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering prompt {template_path}: {e}")
            raise

    async def render_agent_prompt(self, agent_role: str, context: Dict[str, Any]) -> str:
        """
        Convenience method to render a prompt for a specific agent role.
        Expects a template at agents/{agent_role}.md
        """
        template_path = f"agents/{agent_role}.md"
        return await self.render_prompt(template_path, context)
