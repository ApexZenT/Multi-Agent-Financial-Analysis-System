import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def save_to_db(session_factory: sessionmaker, orm_instance) -> bool:
    """
    Generic utility to save a pre-built ORM instance to the database.

    Args:
        session_factory: SQLAlchemy sessionmaker
        orm_instance: An instance of a SQLAlchemy ORM class

    Returns:
        bool: True if saved successfully, False otherwise
    """
    with session_factory() as session:
        try:
            session.add(orm_instance)
            session.commit()
            logger.info("Saved ORM instance: %s", orm_instance)
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error("Failed to save ORM instance: %s | Error: %s", orm_instance, e)
            return False
