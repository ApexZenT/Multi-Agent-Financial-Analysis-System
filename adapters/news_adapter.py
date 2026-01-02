import requests
from models.dto import NewsDTO
from typing import List
from Utils.datetime_utils import parse_datetime
import logging

logger = logging.getLogger(__name__)


class NewsAdapter:
    """Adapter for fetching and normalizing financial news from external APIs."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        logger.info("Initialized NewsAdapter with provided API key.")

    def fetch_news(self, endpoint: str, params: dict) -> List[NewsDTO]:
        """Fetch news from an API endpoint and return as list of NewsDTOs."""
        params["apiKey"] = self.api_key
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            articles = self._parse_articles(response.json())
            logger.info("Fetched %d articles from endpoint %s", len(articles), endpoint)
            return articles
        except requests.RequestException as e:
            logger.error("Request failed for endpoint %s: %s", endpoint, e)
            return []
        except Exception as e:
            logger.error("Unexpected error while fetching news: %s", e)
            return []

    def _parse_articles(self, response_json: dict) -> List[NewsDTO]:
        """Parse the JSON response into a list of NewsDTO objects."""
        articles = response_json.get("articles", [])
        news_list = []
        for a in articles:
            try:
                news_item = NewsDTO(
                    title=a.get("title"),
                    description=a.get("description"),
                    source=a.get("source", {}).get("name"),
                    publishedAt=parse_datetime(a.get("publishedAt")),
                    url=a.get("url"),
                )
                news_list.append(news_item)
            except Exception as e:
                logger.warning("Failed to parse article: %s", e)
        return news_list
