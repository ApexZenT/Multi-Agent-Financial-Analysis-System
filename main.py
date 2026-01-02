import logging
from agents.base import Agent
from agents.evaluator import Evaluator
from agents.optimizer import Optimizer
from agents.coordinator import Coordinator
from agents.decision_maker import DecisionMaker
from agents.analyst import Analyst
from agents.senior_researcher import SeniorResearcher
from agents.writer import Writer
from config.db_config import init_db

# Setup logging
logger = logging.getLogger(__name__)

class MultiAgentTeam:
    def __init__(self):
        # Instantiate agents
        self.coordinator = Coordinator()
        self.researcher = SeniorResearcher()
        self.analyst = Analyst()
        self.decision_maker = DecisionMaker()
        self.evaluator = Evaluator()
        self.optimizer = Optimizer()
        self.writer = Writer()

        # Wire the team
        self.coordinator.add_agent(self.researcher)
        self.coordinator.add_agent(self.analyst)
        self.coordinator.add_agent(self.decision_maker)
        self.coordinator.add_agent(self.evaluator)
        self.coordinator.add_agent(self.optimizer)
        self.coordinator.add_agent(self.writer)


        logger.info("Multi-agent team created!")

    def execute_project(self, project_description: str):
        logger.info(f"EXECUTING PROJECT: {project_description}")
        logger.info("=" * 60)

        result = {}
        try:
            # Step 1: Coordinator delegates project
            result["coordination"] = self.coordinator.delegate_project(
                project_description
            )
            print(result["coordination"])
        except Exception as e:
            result["coordination"] = f"[Error] {e}"
            logger.error("Coordinator error: %s", e)

        try:
            # Step 2: SeniorResearcher gathers research
            result["research"] = self.researcher.research_stock(project_description)
        except Exception as e:
            result["research"] = f"[Error] {e}"
            logger.error("Researcher error: %s", e)

        try:
            # Step 3: Analyst processes the research
            analyst_inputs = result.get("research", "")
            result["analysis"] = self.researcher.send_to(self.analyst, analyst_inputs)
        except Exception as e:
            result["analysis"] = f"[Error] {e}"
            logger.error("Analyst error: %s", e)

        try:
            # Step 4: DecisionMaker generates decision/recommendation
            inputs = (
                project_description,
                result.get("research", ""),
                result.get("analysis", ""),
            )
            result["decision"] = self.analyst.send_to(self.decision_maker, inputs)
        except Exception as e:
            result["decision"] = f"[Error] {e}"
            logger.error("DecisionMaker error: %s", e)

        try:
            # Step 5a: Evaluator reviews the outputs
            eval_inputs = (*inputs, result.get("decision", ""))
            evaluation_feedback = self.decision_maker.send_to(
                self.evaluator, eval_inputs
            )

            # Step 5b: Optimizer refines summaries based on evaluation
            opt_inputs = (*inputs, result.get("decision", ""), evaluation_feedback)
            result["raw_output"] = self.evaluator.send_to(
                self.optimizer, opt_inputs
            )

        except Exception as e:
            result["raw_output"] = f"[Error] {e}"
            logger.error("Evaluator or Optimizer error: %s", e)

        try:
            # Step 6: Writer agent
            result["report"] = self.optimizer.send_to(
                self.writer, result["raw_output"]
            )
        except Exception as e:
            result["report"] = f"[Error] {e}"
            logger.error("Writer error: %s", e)
        logger.info("PROJECT EXECUTION COMPLETED!")
        return result

    def show_team_status(self):
        logger.info("TEAM STATUS")
        agents = [
        self.coordinator,
        self.researcher,
        self.analyst,
        self.decision_maker,
        self.evaluator,
        self.optimizer,
        self.writer
    ]

        for agent in agents:
            tasks_completed = len(getattr(agent, "memory", {}))
            logger.info(
                "  %s (%s): %d tasks completed",
                agent.name,
                getattr(agent, "role", "N/A"),
                tasks_completed,
            )


if __name__ == "__main__":
    # Initialize DB
    init_db()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    team = MultiAgentTeam()
    project_result = team.execute_project("Analyze AAPL")
    team.show_team_status()

    logger.info("Project Result Summary:")
    for k, v in project_result.items():
        logger.info("%s: %s", k, v)
