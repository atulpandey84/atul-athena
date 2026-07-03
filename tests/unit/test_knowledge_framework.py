import pytest
import os
from athena.core.knowledge import KnowledgeManager, KnowledgeAsset

@pytest.mark.asyncio
async def test_knowledge_indexing(tmp_path):
    # Setup temporary knowledge base
    kb_dir = tmp_path / "knowledge"
    kb_dir.mkdir()
    pattern_file = kb_dir / "test_pattern.md"
    pattern_file.write_text("""---
title: Test Pattern
category: Pattern
version: 1.0
tags: [test, mock]
---
# Test Content
""")

    manager = KnowledgeManager(knowledge_base_path=str(kb_dir))
    await manager.index_assets()

    assert len(manager._assets) == 1
    asset = await manager.get_asset_by_title("Test Pattern")
    assert asset is not None
    assert asset.category == "Pattern"
    assert "test" in asset.tags
    assert "# Test Content" in asset.content

@pytest.mark.asyncio
async def test_knowledge_retrieval_by_category():
    manager = KnowledgeManager()
    # Mocking assets directly for retrieval test
    asset = KnowledgeAsset(
        title="Mock Asset",
        category="Security",
        version="1.0",
        tags=["sec"],
        content="...",
        filepath="test.md"
    )
    manager._assets["test.md"] = asset

    sec_assets = await manager.get_assets_by_category("Security")
    assert len(sec_assets) == 1
    assert sec_assets[0].title == "Mock Asset"

    empty_assets = await manager.get_assets_by_category("NonExistent")
    assert len(empty_assets) == 0

@pytest.mark.asyncio
async def test_knowledge_retrieval_by_tag():
    manager = KnowledgeManager()
    asset = KnowledgeAsset(
        title="Tagged Asset",
        category="General",
        version="1.1",
        tags=["cloud", "aws"],
        content="...",
        filepath="cloud.md"
    )
    manager._assets["cloud.md"] = asset

    aws_assets = await manager.get_assets_by_tag("aws")
    assert len(aws_assets) == 1

    cloud_assets = await manager.get_assets_by_tag("cloud")
    assert len(cloud_assets) == 1

    missing_assets = await manager.get_assets_by_tag("azure")
    assert len(missing_assets) == 0
