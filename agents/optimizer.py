from agents.base import Agent
import logging

logger = logging.getLogger(__name__)


class Optimizer(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("Optimizer", "optimization agent", model_type)
        logger.info("Initialized Optimizer agent")

    def optimize(
        self,
        query: str,
        senior_summary: str,
        analyst_summary: str,
        decision_output: dict,
        evaluation_feedback: dict,
    ) -> str:
        logger.info("Optimizer optimizing query: %s", query)
        prompt = f"""
        You are an optimizer for investment research.
        Improve the summaries based on evaluation feedback:

        Senior Summary: {senior_summary}
        Analyst Insights: {analyst_summary}
        Decision Output: {decision_output}
        Evaluation Feedback: {evaluation_feedback}

        Provide a refined summary or actionable recommendations.
        """
        kwargs = {"agent_name": self.name, "context": "optimize"}
        return self.process(prompt, **kwargs)

    def run_task(self, input_data: tuple) -> str:
        query, senior_summary, analyst_summary, decision_output, evaluation_feedback = (
            input_data
        )
        return self.optimize(
            query, senior_summary, analyst_summary, decision_output, evaluation_feedback
        )
