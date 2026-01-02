from agents.base import Agent
import logging

logger = logging.getLogger(__name__)


class DecisionMaker(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("DecisionMaker", "investment decision analyst", model_type)
        logger.info("Initialized DecisionMaker agent")

    def make_decision(
        self, query: str, senior_summary: str, analyst_summary: str
    ) -> str:
        """
        Analyze the senior researcher's summary and analyst's insights to produce
        actionable investment decisions.
        Returns the raw model output as a string.
        """
        logger.info("DecisionMaker analyzing query: %s", query)

        prompt = f"""
        You are an investment decision analyst.
        Based on the following inputs, suggest an action for the query {query}.
        Choose one of Buy, Hold, or Sell.
        Provide a short rationale (1-2 sentences) and risk level (Low, Medium, High).

        Senior Researcher's Summary:
        {senior_summary}

        Analyst's Insights:
        {analyst_summary}
        """

        kwargs = {"agent_name": self.name, "context": "make_decision"}

        decision = self.process(prompt, **kwargs)

        logger.info("DecisionMaker completed decision for query: %s", query)
        logger.debug("DecisionMaker output: %s", decision[:300])

        return decision

    def run_task(self, input_data: tuple) -> str:
        """
        Receive input data (query, senior_summary, analyst_summary)
        and produce an investment decision.
        """
        if not isinstance(input_data, (tuple, list)) or len(input_data) != 3:
            logger.error("Invalid input format for DecisionMaker: %s", input_data)
            raise ValueError(
                "Expected input_data as a tuple: (query, senior_summary, analyst_summary)"
            )

        query, senior_summary, analyst_summary = input_data
        logger.debug("Running DecisionMaker task for query: %s", query)
        return self.make_decision(query, senior_summary, analyst_summary)
