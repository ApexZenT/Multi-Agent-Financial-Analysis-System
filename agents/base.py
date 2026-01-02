import json
import datetime
import logging
from gpt4all import GPT4All
from Utils.properties_util import PropertiesUtil
from models.orm import AgentMemory
from Utils.db_util import save_to_db
from config.db_config import SessionAgentMemory
from models.dto import AgentMemoryDTO

# -------------------------------------------------------------------
# Global model instance (loaded once and reused across agents)
# -------------------------------------------------------------------
MODEL = GPT4All(model_name="Phi-3-mini-4k-instruct.Q4_0.gguf", device='cpu')

# -------------------------------------------------------------------
# Setup module-level logger
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)
mock = True

class Agent:
    """Base class for all AI agents in the multi-agent framework."""

    def __init__(
        self, name: str, role: str, model: str = "gguf-model-falcon-q4_0.gguf"
    ):
        self.name = name
        self.role = role
        self.model = MODEL  # use the preloaded model instance
        logger.info("Initialized agent: %s (%s)", self.name, self.role)
        self.task_counter = {}
    # -------------------------------------------------------------------
    # Core LLM call
    # -------------------------------------------------------------------
    def call_llm(self, prompt: str) -> str:
        """Send a prompt to the LLM and return its response."""
        if mock:
            return f"Mock response from {self.name}: {prompt[:50]}..."
        try:
            result = self.model.generate(prompt)
            logger.debug("LLM response for %s: %s...", self.name, result[:80])
            return result
        except Exception as e:
            logger.error("LLM call failed for %s: %s", self.name, e, exc_info=True)
            return f"Mock response from {self.name}: {prompt[:50]}..."

    # -------------------------------------------------------------------
    # Process & persist memory
    # -------------------------------------------------------------------
    def process(self, prompt: str, **kwargs) -> str:
        """Process a prompt through the agent and store its memory."""
        logger.info(
            "Agent %s processing context: %s",
            self.name,
            kwargs.get("context", "UnknownContext"),
        )

        result = self.call_llm(prompt)

        memory_dto = AgentMemoryDTO(
            agent_name=kwargs.get("agent_name", self.name),
            context=kwargs.get("context", "UnknownContext"),
            inputs=prompt,
            output=result,
            timestamp=datetime.datetime.now().isoformat(),
        )

        # Convert DTO to ORM instance
        memory_entry = AgentMemory(**memory_dto.__dict__)
        save_to_db(SessionAgentMemory, memory_entry)
        logger.debug(
            "Memory saved for agent %s under context '%s'",
            self.name,
            kwargs.get("context", "UnknownContext"),
        )
        return result

    # -------------------------------------------------------------------
    # Default task handler
    # -------------------------------------------------------------------
    def run_task(self, input_data: str) -> str:
        """Default generic task executor."""
        logger.info("Agent %s running task with input: %s", self.name, input_data[:80])
        prompt = f"Process this as a {self.role}: {input_data}"
        return self.process(prompt)

    # -------------------------------------------------------------------
    # Send data between agents
    # -------------------------------------------------------------------
    def send_to(self, other_agent, input_data: str) -> str:
        """Send processed data from one agent to another."""
        logger.info(
            "%s → %s | Data length: %d", self.name, other_agent.name, len(input_data)
        )
        return other_agent.run_task(input_data)
