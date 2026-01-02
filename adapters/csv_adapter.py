from models.dto import NewsDTO
import polars as pl
from pathlib import Path
from typing import List
from Utils.datetime_utils import parse_datetime
import logging


class CSVAdapter:
    """
    Adapter for loading and normalizing financial news CSVs
    (e.g., CNBC, Reuters, Bloomberg) into a common schema.
    """

    BASE_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

    _rename_map = {
        "headline": "title",
        "headlines": "title",
        "content": "description",
        "summary_text": "description",
        "summary": "description",
        "date_published": "publishedAt",
        "timestamp": "publishedAt",
        "time": "publishedAt",
    }

    def fetch_news_from_csv(self) -> List[NewsDTO]:
        all_news: List[NewsDTO] = []

        csv_files = list(self.BASE_PATH.glob("*.csv"))
        if not csv_files:
            logger.warning("No CSV files found in %s", self.BASE_PATH)
            return all_news

        logger.info("Found %d CSV files to process.", len(csv_files))

        for csv_file in csv_files:
            try:
                df = pl.read_csv(csv_file)

                # Standardize column names
                df = df.rename(
                    {
                        col: col.replace("-", "_").replace(" ", "_").lower().strip()
                        for col in df.columns
                    }
                )
                df = df.rename(self._rename_map, strict=False)

                filtered_df = df.filter(
                    pl.col("title").is_not_null() & (pl.col("title") != "")
                )

                rows_as_dicts = filtered_df.to_dicts()
                logger.info(
                    "Processing %d rows from CSV file: %s",
                    len(rows_as_dicts),
                    csv_file.name,
                )

                for row in rows_as_dicts:
                    news_item = NewsDTO(
                        title=row.get("title"),
                        publishedAt=parse_datetime(row.get("publishedAt")),
                        description=row.get("description"),
                        source=csv_file.stem,  # use file name as source
                        url=row.get("url"),
                    )
                    all_news.append(news_item)

            except Exception as e:
                logger.error("Error processing CSV file %s: %s", csv_file.name, e)

        logger.info("Total news items fetched from CSVs: %d", len(all_news))
        return all_news


# Example usage
if __name__ == "__main__":
    logger = logging.getLogger()
    if not logger.hasHandlers():  # only configure if not already
        logging.basicConfig(level=logging.INFO)

    adapter = CSVAdapter()
    news_items = adapter.fetch_news_from_csv()
    for item in news_items[:5]:
        logger.info(item)
