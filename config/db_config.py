import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.orm import BaseNews, BaseAgentMemory
from Utils.properties_util import PropertiesUtil

logger = logging.getLogger(__name__)

# Paths
BASE_PATH = Path(__file__).parent.parent / "data" / "processed"
BASE_PATH.mkdir(parents=True, exist_ok=True)

# --- News Database ---
NEWS_DATABASE_URL = f"sqlite:///{BASE_PATH}/news.db"
engine_news = create_engine(
    NEWS_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)
SessionNews = sessionmaker(bind=engine_news, expire_on_commit=False, autoflush=False)

logger.info("News database initialized at %s", NEWS_DATABASE_URL)

# --- Agent Memory Database ---
AGENTMEMORY_DATABASE_URL = f"sqlite:///{BASE_PATH}/agent_memory.db"
engine_agent_memory = create_engine(
    AGENTMEMORY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)
SessionAgentMemory = sessionmaker(
    bind=engine_agent_memory, expire_on_commit=False, autoflush=False
)

logger.info("Agent memory database initialized at %s", AGENTMEMORY_DATABASE_URL)


def init_db():
    """Create all tables. Call this once at startup."""
    BaseNews.metadata.create_all(bind=engine_news)
    BaseAgentMemory.metadata.create_all(bind=engine_agent_memory)
    logger.info("Database tables created successfully")
