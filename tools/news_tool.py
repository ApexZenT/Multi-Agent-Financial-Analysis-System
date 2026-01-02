import logging
from services.news_service import NewsService
from models.dto import NewsDTO
from typing import List
from Utils.properties_util import PropertiesUtil

logger = logging.getLogger(__name__)


class NewsTool:
    """Tool exposing financial news fetching & DB operations."""

    name = "NewsTool"
    description = "Fetch and store financial news via NewsAPI and local DB."

    # Load configuration once
    _config = PropertiesUtil.load_properties()
    _api_key: str = _config.get_property("news_api_key")
    _endpoint_everything: str = _config.get_property("news_api_endpoint_everything")
    _endpoint_top_headlines: str = _config.get_property(
        "news_api_endpoint_top_headlines"
    )

    _service: NewsService = None  # lazy init

    @property
    def service(self):
        """Initialize NewsService lazily."""
        if self._service is None:
            if not self._api_key:
                logger.error("Missing News API key in global-settings.properties")
                raise ValueError("Missing News API key in global-settings.properties")
            logger.info("Initializing NewsService...")
            self._service = NewsService(api_key=self._api_key)
        return self._service

    def fetch_everything(self, **kwargs) -> List[NewsDTO]:
        logger.debug("Fetching everything news with params: %s", kwargs)
        news_items = self.service.fetch_and_store_news(
            self._endpoint_everything, **kwargs
        )
        logger.info("Fetched %d 'everything' news items", len(news_items))
        return news_items

    def fetch_top_headlines(self, **kwargs) -> List[NewsDTO]:
        logger.debug("Fetching top headlines with params: %s", kwargs)
        news_items = self.service.fetch_and_store_news(
            self._endpoint_top_headlines, **kwargs
        )
        logger.info("Fetched %d top headlines", len(news_items))
        return news_items

    def fetch_news(self, source: str = "recent", **kwargs) -> List[NewsDTO]:
        logger.info("Fetching news from source: '%s'", source)
        news: List[NewsDTO] = []

        if source == "recent":
            news.extend(self.fetch_top_headlines(**kwargs))
        elif source == "history":
            news.extend(self.fetch_everything(**kwargs))
            news.extend(self.service.get_stored_news(**kwargs))
        elif source == "db":
            news.extend(self.service.get_stored_news(**kwargs))
        else:
            logger.error("Invalid news source '%s'", source)
            raise ValueError(f"Invalid news source '{source}'")

        # Deduplicate by URL
        seen = set()
        unique_news = []
        for article in news:
            key = getattr(article, "url", None)
            if key and key not in seen:
                seen.add(key)
                unique_news.append(article)

        logger.info("Returning %d unique news articles", len(unique_news))
        return unique_news
