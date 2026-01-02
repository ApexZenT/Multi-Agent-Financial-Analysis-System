import requests
import logging
from Utils.properties_util import PropertiesUtil

logger = logging.getLogger(__name__)


class EconomicDataTool:
    """Tool for fetching economic indicators from FRED API."""

    name = "EconomicDataTool"
    description = "Fetch economic data (GDP, CPI, unemployment, etc.) via FRED API."

    # Load configuration once
    _config = PropertiesUtil.load_properties()
    api_key: str = _config.get_property("fred_api_key")
    fred_endpoint: str = _config.get_property("fred_api_endpoint")

    def fetch_series(
        self, series_id: str, start_date: str = None, end_date: str = None
    ) -> dict:
        """
        Fetch time series data from FRED.

        Args:
            series_id (str): Example 'GDP', 'CPIAUCSL', 'UNRATE'
            start_date (str): 'YYYY-MM-DD'
            end_date (str): 'YYYY-MM-DD'

        Returns:
            dict: Time series data
        """
        params = {"series_id": series_id, "api_key": self.api_key, "file_type": "json"}
        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date

        logger.info(
            "Fetching economic series '%s' from %s", series_id, self.fred_endpoint
        )
        try:
            response = requests.get(
                f"{self.fred_endpoint}/series/observations", params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if "observations" not in data:
                logger.error("No observations found for series %s: %s", series_id, data)
                raise ValueError(f"Error fetching series {series_id}: {data}")
            logger.info(
                "Fetched %d observations for series %s",
                len(data["observations"]),
                series_id,
            )
            return data["observations"]
        except requests.RequestException as e:
            logger.exception("Request failed for series %s: %s", series_id, e)
            raise
