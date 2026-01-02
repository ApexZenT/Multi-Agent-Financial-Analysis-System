from agents.base import Agent
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Writer(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("Writer", "content writer", model_type)
        logger.info("Initialized Writer agent")

    def write_report(self, content: str) -> str:
        """
        Generate a professional report based on the given content.
        """
        logger.info("Writer received content to generate report")
        kwargs = {"agent_name": self.name, "context": "write_report"}

        report = self.process(
            f"Write a professional report based on this analysis:\n{content}", **kwargs
        )

        logger.info("Writer completed report generation")
        logger.debug("Report content (truncated 300 chars): %s", report[:300])
        return report

    def run_task(self, input_data: str) -> str:
        logger.info("Writer running task")
        return self.write_report(input_data)
