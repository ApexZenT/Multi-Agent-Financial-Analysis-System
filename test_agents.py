"""
Test script for EvaluatorOptimizer and Agent
-----------------------------------------------------

This script validates:
- EvaluatorOptimizer's evaluate method.
- Agent's process and insert_data methods with SQLite storage.
"""

import sys
from pathlib import Path
from models.orm import AgentMemory
from config.db_config import SessionAgentMemory

# --- Dynamically add project root to sys.path ---
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

print("Added to sys.path:", PROJECT_ROOT)

# --- Import Agent and EvaluatorOptimizer ---
from agents.base import Agent
from agents.evaluator_optimizer import EvaluatorOptimizer
from agents.coordinator import Coordinator
from agents.decision_maker import DecisionMaker
from agents.analyst import Analyst
from agents.senior_researcher import SeniorResearcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ----------------------------
# 1. Initialize EvaluatorOptimizer
# ----------------------------
print("Initializing EvaluatorOptimizer...")
evaluator = EvaluatorOptimizer()

# ----------------------------
# 2. Define Mock Inputs
# ----------------------------
senior_summary = "Apple's revenue grew 5% YoY, driven by strong iPhone sales."
analyst_summary = "High demand for AI features boosts Apple's growth potential."
decision_output = {
    "symbol": "AAPL",
    "suggestion": "Buy",
    "rationale": "Strong fundamentals and AI innovation.",
    "risk_level": "Medium",
}

# ----------------------------
# 3. Test EvaluatorOptimizer.evaluate
# ----------------------------
print("\nTesting EvaluatorOptimizer.evaluate...")
try:
    evaluation = evaluator.evaluate(senior_summary, analyst_summary, decision_output)
    co
    print("\n--- Evaluation Result ---")
    print(f"Feedback:\n{evaluation}\n")

    # Verify database storage
    print("Verifying SQLite storage...")

    entries = (
        SessionAgentMemory()
        .query(AgentMemory)
        .filter_by(agent_name="EvaluatorOptimizer")
        .all()
    )
    print("\n--- Database Entries for EvaluatorOptimizer ---")
    for entry in entries:
        print(
            f"ID: {entry.id}, Context: {entry.context}, Inputs: {entry.inputs}, Output: {entry.output}, Timestamp: {entry.timestamp}"
        )
    SessionAgentMemory().close()

except Exception as e:
    print("Error during evaluation:", e)
