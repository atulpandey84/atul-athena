import logging
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DiagramType(str, Enum):
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    CLASS = "class"
    ENTITY_RELATIONSHIP = "er"

class DiagramNode(BaseModel):
    id: str
    label: str
    type: Optional[str] = None

class DiagramEdge(BaseModel):
    from_node: str
    to_node: str
    label: Optional[str] = None

class DiagramModel(BaseModel):
    title: str
    type: DiagramType
    nodes: List[DiagramNode]
    edges: List[DiagramEdge]

class DiagramEngine:
    """
    Generates visual diagrams from structured architectural models.
    """
    async def generate_mermaid(self, model: DiagramModel) -> str:
        """
        Convert a DiagramModel into Mermaid syntax.
        """
        logger.info(f"Generating Mermaid {model.type} diagram: {model.title}")

        if model.type == DiagramType.FLOWCHART:
            return self._generate_mermaid_flowchart(model)
        elif model.type == DiagramType.SEQUENCE:
            return self._generate_mermaid_sequence(model)
        else:
            raise NotImplementedError(f"Mermaid generation for {model.type} not yet implemented.")

    def _generate_mermaid_flowchart(self, model: DiagramModel) -> str:
        lines = ["graph TD"]
        for node in model.nodes:
            lines.append(f"    {node.id}[{node.label}]")
        for edge in model.edges:
            connection = f" --> "
            if edge.label:
                connection = f" -- {edge.label} --> "
            lines.append(f"    {edge.from_node}{connection}{edge.to_node}")
        return "\n".join(lines)

    def _generate_mermaid_sequence(self, model: DiagramModel) -> str:
        lines = ["sequenceDiagram"]
        for node in model.nodes:
            lines.append(f"    participant {node.id} as {node.label}")
        for edge in model.edges:
            label = f": {edge.label}" if edge.label else ": interaction"
            lines.append(f"    {edge.from_node}->>{edge.to_node}{label}")
        return "\n".join(lines)
