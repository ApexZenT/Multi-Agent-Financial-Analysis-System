import logging
from typing import List
from adapters.news_adapter import NewsAdapter
from dao.news_dao import NewsDB
from models.dto import NewsDTO
from Utils.properties_util import PropertiesUtil

logger = logging.getLogger(__name__)  # module-level logger


class NewsService:
    """Handles all business logic related to fetching and storing news."""

    _config = PropertiesUtil.load_properties()
    load_limit: int = int(_config.get_property("news_load_limit", 1000))
    load_csv_flag: bool = (
        _config.get_property("load_csv_to_db", "false").lower() == "true"
    )

    def __init__(self, api_key: str):
        self.adapter = NewsAdapter(api_key)
        self.db = NewsDB()

        if self.load_csv_flag:
            logger.info("CSV-to-DB load enabled. Starting initial load...")
            self._load_csv_to_db()
        else:
            logger.info("CSV-to-DB load disabled. Skipping initial load.")

    def _load_csv_to_db(self):
        """Private method to load CSV into DB only once."""
        from adapters.csv_adapter import CSVAdapter  # lazy import to avoid circular dep

        csv_adapter = CSVAdapter()
        news_records = csv_adapter.fetch_news_from_csv()
        self.db.insert_news(news_records)
        logger.info("Inserted %d CSV records into DB.", len(news_records))

    def fetch_and_store_news(self, endpoint: str, **kwargs) -> List[NewsDTO]:
        """Fetch news using flexible parameters and optionally store to DB."""
        logger.debug("Fetching news from endpoint: %s | Params: %s", endpoint, kwargs)
        news_items = self.adapter.fetch_news(endpoint, kwargs)
        self.db.insert_news(news_items)
        logger.info("Fetched and stored %d news items.", len(news_items))
        return news_items

    def get_stored_news(self, **kwargs) -> List[NewsDTO]:
        """Fetch stored news with flexible filtering options."""
        limit = kwargs.get("limit", self.load_limit)
        logger.debug("Fetching %d stored news records from DB.", limit)
        news = self.db.fetch_news(limit=limit)
        logger.info("Retrieved %d stored news records.", len(news))
        return news
