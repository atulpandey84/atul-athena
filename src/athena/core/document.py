import logging
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .consensus import ConsensusReport

logger = logging.getLogger(__name__)

class DocumentOutput(BaseModel):
    filename: str
    format: str
    content: Any  # File path or binary data
    metadata: Dict[str, Any] = {}

class DocumentEngine:
    """
    Transforms architectural outputs into professional consulting deliverables.
    """
    def __init__(self, output_dir: str = "site/deliverables"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    async def generate_markdown_report(self, report: ConsensusReport) -> DocumentOutput:
        """
        Generate a Markdown representation of a Consensus Report.
        """
        logger.info(f"Generating Markdown report for session {report.session_id}")

        md_content = f"""# {report.final_recommendation.title if report.final_recommendation else 'Architectural Decision'}

## Executive Summary
**Status**: {report.status.upper()}
**Decision Maker**: {report.decision_maker_id}

### Rationale
{report.rationale}

"""
        if report.final_recommendation:
            rec = report.final_recommendation
            md_content += f"""
## Detailed Recommendation

### Pros
{chr(10).join(['- ' + p for p in rec.pros])}

### Cons
{chr(10).join(['- ' + c for c in rec.cons])}

### Alternatives
{chr(10).join(['- ' + a for a in rec.alternatives])}

### Tradeoffs
{chr(10).join(['- ' + t for t in rec.tradeoffs])}

### Impact Assessment
- **Risk**: {rec.risk}
- **Cost**: {rec.cost}
- **Operational**: {rec.operational_impact}
- **Security**: {rec.security_impact}
- **Migration**: {rec.migration_impact}

### Final Recommendation
{rec.final_recommendation}
"""

        filename = f"report_{report.session_id}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return DocumentOutput(
            filename=filename,
            format="markdown",
            content=filepath,
            metadata={"session_id": report.session_id}
        )

    async def generate_deliverable_package(self, report: ConsensusReport, formats: List[str]) -> List[DocumentOutput]:
        """
        Generate multiple deliverables for a given report.
        """
        outputs = []
        if "markdown" in formats or "md" in formats:
            outputs.append(await self.generate_markdown_report(report))

        # Placeholders for DOCX, PPTX, PDF in future phases
        return outputs
