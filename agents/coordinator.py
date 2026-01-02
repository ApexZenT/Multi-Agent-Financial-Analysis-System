import logging
from agents.base import Agent

logger = logging.getLogger(__name__)


class Coordinator(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("Boss", "coordinator", model_type)
        self.team = []

    def add_agent(self, agent):
        """Add an agent to the coordination team."""
        self.team.append(agent)
        logger.info(f"➕ Added {agent.name} to team.")

    def delegate_project(self, project_description):
        """Create a research plan and delegate tasks to all team members."""
        logger.info(f"[{self.name}] Delegating project: {project_description}")

        # Generate plan
        plan_prompt = f"Create a step-by-step research plan for: {project_description}"
        plan_kwargs = {"agent_name": self.name, "context": "delegate_project"}

        plan = self.process(plan_prompt, **plan_kwargs)
        logger.info(f"[{self.name}] Generated project plan.")

        # Delegate tasks to each team member
        results = {}
        for agent in self.team:
            task = f"Work on project '{project_description}' using your {agent.role} skills."
            task_kwargs = {"agent_name": agent.name, "context": "delegate_project"}

            logger.info(f"[{self.name}] Assigning task to {agent.name} ({agent.role})")
            results[agent.name] = agent.process(task, **task_kwargs)
            logger.info(f"[{agent.name}] Task completed.")

        logger.info(
            f"[{self.name}] Delegation complete for project: {project_description}"
        )
        return {"plan": plan, "results": results}
