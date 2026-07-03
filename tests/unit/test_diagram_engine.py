import pytest
import asyncio
from athena.core.diagram import DiagramEngine, DiagramModel, DiagramType, DiagramNode, DiagramEdge

@pytest.mark.asyncio
async def test_mermaid_flowchart_generation():
    engine = DiagramEngine()

    model = DiagramModel(
        title="Test Flow",
        type=DiagramType.FLOWCHART,
        nodes=[
            DiagramNode(id="A", label="Start"),
            DiagramNode(id="B", label="End")
        ],
        edges=[
            DiagramEdge(from_node="A", to_node="B", label="proceed")
        ]
    )

    output = await engine.generate_mermaid(model)
    assert "graph TD" in output
    assert "A[Start]" in output
    assert "A -- proceed --> B" in output

@pytest.mark.asyncio
async def test_mermaid_sequence_generation():
    engine = DiagramEngine()

    model = DiagramModel(
        title="Test Sequence",
        type=DiagramType.SEQUENCE,
        nodes=[
            DiagramNode(id="User", label="Client"),
            DiagramNode(id="API", label="Server")
        ],
        edges=[
            DiagramEdge(from_node="User", to_node="API", label="GET /data")
        ]
    )

    output = await engine.generate_mermaid(model)
    assert "sequenceDiagram" in output
    assert "participant User as Client" in output
    assert "User->>API: GET /data" in output

@pytest.mark.asyncio
async def test_unsupported_diagram_type():
    engine = DiagramEngine()
    model = DiagramModel(title="X", type=DiagramType.CLASS, nodes=[], edges=[])

    with pytest.raises(NotImplementedError):
        await engine.generate_mermaid(model)
