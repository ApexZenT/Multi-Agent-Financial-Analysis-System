import logging
import yfinance as yf

logger = logging.getLogger(__name__)


class StockTool:
    """A tool for fetching stock data using yfinance."""

    name = "StockAPI"
    description = (
        "A tool for fetching stock data. "
        "Use this tool to get historical stock prices, current stock prices, and other financial data."
    )

    def _get_ticker(self, symbol: str):
        """Helper method to validate and return a yfinance Ticker object."""
        try:
            ticker = yf.Ticker(symbol)
            if not ticker.info:
                raise ValueError(f"Ticker symbol '{symbol}' not found or has no info.")
            return ticker
        except Exception as e:
            logger.error("Error fetching ticker '%s': %s", symbol, e)
            raise

    def fetch_historical_data(
        self, symbol: str, period: str = "1yr", interval: str = "1d"
    ) -> dict:
        """Fetch historical stock data for a given ticker symbol."""
        logger.info(
            "Fetching historical data for %s | period=%s, interval=%s",
            symbol,
            period,
            interval,
        )
        ticker = self._get_ticker(symbol)
        try:
            history = ticker.history(period=period, interval=interval)
            data = history.to_dict()
            logger.debug(
                "Historical data fetched for %s: %d entries", symbol, len(history)
            )
            return data
        except Exception as e:
            logger.error("Error fetching historical data for %s: %s", symbol, e)
            raise

    def fetch_financial_info(self, symbol: str) -> dict:
        """Fetch financial statements for a given ticker symbol."""
        logger.info("Fetching financial info for %s", symbol)
        ticker = self._get_ticker(symbol)
        try:
            financials = {
                "income_statement": ticker.financials,
                "balance_sheet": ticker.balance_sheet,
                "cashflow": ticker.cashflow,
            }
            logger.debug("Financial info fetched for %s", symbol)
            return financials
        except Exception as e:
            logger.error("Error fetching financial info for %s: %s", symbol, e)
            raise

    def fetch_symbol_info(self, symbol: str) -> dict:
        """Fetch general information for a given ticker symbol."""
        logger.info("Fetching symbol info for %s", symbol)
        ticker = self._get_ticker(symbol)
        try:
            info = ticker.info
            data = {
                "name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "beta": info.get("beta"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
            }
            logger.debug("Symbol info fetched for %s: %s", symbol, data)
            return data
        except Exception as e:
            logger.error("Error fetching symbol info for %s: %s", symbol, e)
            raise
