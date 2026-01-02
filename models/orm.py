from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

BaseNews = declarative_base()
BaseAgentMemory = declarative_base()


# Define the News ORM model
class News(BaseNews):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    source = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    publishedAt = Column(DateTime, index=True)


class AgentMemory(BaseAgentMemory):
    __tablename__ = "agent_memory"

    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    context = Column(String)
    inputs = Column(Text)
    output = Column(Text)
    timestamp = Column(String)
