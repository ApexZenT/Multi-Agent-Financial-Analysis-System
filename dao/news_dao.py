from models.orm import News
from models.dto import NewsDTO
from typing import List, Optional
from config.db_config import SessionNews
import logging

logger = logging.getLogger(__name__)


class NewsDB:
    """DAO / DAL for News table using SQLAlchemy ORM."""

    def __init__(self):
        self.session = SessionNews()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def insert_news(self, news_items: List[NewsDTO]):
        """Insert multiple news records into the database in batches, skipping duplicates."""
        if not news_items:
            logger.info("No news items to process.")
            return

        titles_set = {item.title for item in news_items if item.title}
        titles_list = list(titles_set)

        # Check for existing titles in batches
        existing_titles = set()
        logger.info("Checking for existing titles in batches...")
        chunk_size_lookup = 500
        for i in range(0, len(titles_list), chunk_size_lookup):
            batch_titles = titles_list[i : i + chunk_size_lookup]
            existing_in_batch = (
                self.session.query(News.title)
                .filter(News.title.in_(batch_titles))
                .all()
            )
            existing_titles.update(title for (title,) in existing_in_batch)
        logger.info("Found %d existing articles.", len(existing_titles))

        # Prepare new records
        new_records = [
            {
                "title": item.title,
                "publishedAt": item.publishedAt,
                "description": item.description,
                "source": item.source,
                "url": item.url,
            }
            for item in news_items
            if item.title not in existing_titles
        ]

        if not new_records:
            logger.info("No new articles to insert.")
            return

        # Bulk insert in chunks
        chunk_size_insert = 500
        try:
            for i in range(0, len(new_records), chunk_size_insert):
                batch = new_records[i : i + chunk_size_insert]
                self.session.bulk_insert_mappings(News, batch)
                logger.info(
                    "Inserted batch %d with %d items.",
                    i // chunk_size_insert + 1,
                    len(batch),
                )
            self.session.commit()
            logger.info("All new news items inserted successfully.")
        except Exception as e:
            self.session.rollback()
            logger.error("Error during bulk insert: %s", e)
            raise

    def fetch_news(
        self, limit: int = 1000, source: Optional[str] = None, q: Optional[str] = None
    ) -> List[NewsDTO]:
        """Fetch news records from the database."""
        query = self.session.query(News)
        if source:
            query = query.filter(News.source == source)
        if q:
            query = query.filter(News.title.ilike(f"%{q}%"))

        records = query.limit(limit).all()
        news_dtos = [
            NewsDTO(
                title=r.title,
                publishedAt=r.publishedAt,
                description=r.description,
                source=r.source,
                url=r.url,
            )
            for r in records
        ]
        logger.info("Fetched %d news records from DB.", len(news_dtos))
        return news_dtos

    def close(self):
        self.session.close()
        logger.info("Database session closed.")
