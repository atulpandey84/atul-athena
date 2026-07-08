import logging
import json
import time
from typing import Any, Dict

class StructuredLogger:
    """
    Utility for generating consistent structured JSON logs for ATHENA.
    """
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = logging.getLogger(component_name)

    def _format(self, level: str, message: str, project_id: str = "N/A", trace_id: str = "N/A", data: Dict[str, Any] = None) -> str:
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": level,
            "component": self.component_name,
            "project_id": project_id,
            "trace_id": trace_id,
            "message": message,
            "data": data or {}
        }
        return json.dumps(log_entry)

    def info(self, message: str, **kwargs):
        self.logger.info(self._format("INFO", message, **kwargs))

    def error(self, message: str, **kwargs):
        self.logger.error(self._format("ERROR", message, **kwargs))

    def debug(self, message: str, **kwargs):
        self.logger.debug(self._format("DEBUG", message, **kwargs))
