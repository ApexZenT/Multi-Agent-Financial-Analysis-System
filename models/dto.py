from typing import Optional
from dataclasses import dataclass
from datetime import datetime


# --- News DTO ---
@dataclass
class NewsDTO:
    title: str
    publishedAt: Optional[datetime] = None
    description: Optional[str] = None
    source: Optional[str] = None  # for CSV - file name, for API - source name
    url: Optional[str] = None


# -- Agent Memory DTO ---
@dataclass
class AgentMemoryDTO:
    agent_name: str
    context: str
    inputs: str
    output: str
    timestamp: Optional[str] = None
