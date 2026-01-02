from agents.base import Agent
import logging

logger = logging.getLogger(__name__)


class Evaluator(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("Evaluator", "evaluation agent", model_type)
        logger.info("Initialized Evaluator agent")

    def evaluate(
        self,
        query: str,
        senior_summary: str,
        analyst_summary: str,
        decision_output: dict,
    ) -> dict:
        logger.info("Evaluator evaluating query: %s", query)
        prompt = f"""
        You are an evaluator for investment research.
        Evaluate the following for query: {query}:

        Senior Researcher's Summary:
        {senior_summary}

        Analyst's Insights:
        {analyst_summary}

        Decision Maker's Suggestion:
        {decision_output}

        Check for:
        - Completeness
        - Clarity
        - Accuracy
        - Suggestions for improvement

        Provide concise feedback.
        """
        kwargs = {"agent_name": self.name, "context": "evaluate"}
        feedback_text = self.process(prompt, **kwargs)
        return {
            "senior_summary_feedback": feedback_text,
            "analyst_summary_feedback": feedback_text,
            "decision_feedback": feedback_text,
        }

    def run_task(self, input_data: tuple) -> dict:
        return self.evaluate(*input_data)
