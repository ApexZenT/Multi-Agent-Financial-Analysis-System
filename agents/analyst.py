import logging
from agents.base import Agent

logger = logging.getLogger(__name__)


class Analyst(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("Analyst", "financial analyst", model_type)

    def run_task(self, research_summary: str) -> str:
        """
        Receive input from Researcher and provide analysis insights.
        """
        prompt = f"""
        You are a financial analyst. Based on the following research summaries,
        provide insights on trends, risks, and potential opportunities:

        {research_summary}
        """
        kwargs = {"agent_name": self.name, "context": "run_task"}

        logger.info(f"[{self.name}] Starting analysis with context: {kwargs}")
        analysis = self.process(prompt, **kwargs)
        logger.info(f"[{self.name}] Analysis complete. Output: {analysis[:200]}...")

        return analysis
