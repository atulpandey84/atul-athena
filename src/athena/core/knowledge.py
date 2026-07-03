import os
import yaml
import logging
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

class KnowledgeAsset(BaseModel):
    title: str
    category: str
    version: str
    tags: List[str]
    content: str
    filepath: str

    @field_validator('version', mode='before')
    @classmethod
    def version_to_string(cls, v: Any) -> str:
        return str(v)

class KnowledgeManager:
    """
    Manages access to the ATHENA Knowledge Framework assets.
    """
    def __init__(self, knowledge_base_path: str = "docs/knowledge"):
        self.knowledge_base_path = knowledge_base_path
        self._assets: Dict[str, KnowledgeAsset] = {}

    async def index_assets(self):
        """Index all knowledge assets in the knowledge base directory."""
        logger.info(f"Indexing knowledge assets from {self.knowledge_base_path}")
        if not os.path.exists(self.knowledge_base_path):
            logger.warning(f"Knowledge base path {self.knowledge_base_path} does not exist.")
            return

        for root, _, files in os.walk(self.knowledge_base_path):
            for file in files:
                if file.endswith(".md"):
                    await self._process_file(os.path.join(root, file))

    async def _process_file(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic YAML front-matter extraction
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()

                    asset = KnowledgeAsset(
                        title=str(metadata.get('title', 'Unknown')),
                        category=str(metadata.get('category', 'General')),
                        version=metadata.get('version', '1.0'),
                        tags=metadata.get('tags', []) if isinstance(metadata.get('tags'), list) else [],
                        content=body,
                        filepath=filepath
                    )
                    self._assets[filepath] = asset
                    logger.debug(f"Indexed asset: {asset.title}")
        except Exception as e:
            logger.error(f"Error processing knowledge asset {filepath}: {e}")

    async def get_assets_by_category(self, category: str) -> List[KnowledgeAsset]:
        """Retrieve assets belonging to a specific category."""
        return [asset for asset in self._assets.values() if asset.category.lower() == category.lower()]

    async def get_assets_by_tag(self, tag: str) -> List[KnowledgeAsset]:
        """Retrieve assets containing a specific tag."""
        return [asset for asset in self._assets.values() if tag.lower() in [t.lower() for t in asset.tags]]

    async def get_asset_by_title(self, title: str) -> Optional[KnowledgeAsset]:
        """Retrieve a specific asset by its title."""
        for asset in self._assets.values():
            if asset.title.lower() == title.lower():
                return asset
        return None
