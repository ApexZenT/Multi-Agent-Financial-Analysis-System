import logging
from tools import stock_tool, news_tool, economic_tool
from agents.base import Agent

logger = logging.getLogger(__name__)


class SeniorResearcher(Agent):
    def __init__(self, model_type: str = "mock"):
        super().__init__("SeniorResearcher", "lead researcher", model_type)
        self.stock_agent = StockAgent()
        self.news_agent = NewsAgent()
        self.economic_agent = EconomicAgent()

    def select_research_source(self, query: str) -> list[str]:
        prompt = f"""
        You are a senior researcher. Decide the best research source(s) for this query: {query}.
        Options: Stock (ticker data), News (recent or historical headlines), Economic data (GDP, CPI, unemployment, etc.)
        You can choose more than one. Return the selected sources as a comma-separated list.
        """
        kwargs = {"agent_name": self.name, "context": "select_research_source"}
        choice_text = self.process(prompt, **kwargs)

        sources = [c.strip().lower() for c in choice_text.split(",")]
        valid_sources = {"stock", "news", "economic"}
        selected_sources = [s for s in sources if s in valid_sources]
        if not selected_sources:
            selected_sources = ["news", "economic"]

        logger.info(
            "Selected research sources for query '%s': %s", query, selected_sources
        )
        return selected_sources

    def research_stock(self, query: str) -> str:
        logger.info("--- Senior Researcher Delegating Tasks for query: %s ---", query)
        selected_sources = self.select_research_source(query)
        stock_summary, news_summary, economic_summary = "", "", ""

        if "stock" in selected_sources:
            stock_summary = self.stock_agent.run_task(query)

        if "news" in selected_sources:
            news_summary = self.news_agent.run_task(query)

        if "economic" in selected_sources:
            economic_prompt = f"Provide economic indicators relevant to {query} and choose an appropriate timeframe."
            economic_summary = self.economic_agent.run_task(economic_prompt)

        raw_combined_text = ""
        if stock_summary:
            raw_combined_text += f"Stock Summary:\n{stock_summary}\n\n"
        if news_summary:
            raw_combined_text += f"News Summary:\n{news_summary}\n\n"
        if economic_summary:
            raw_combined_text += f"Economic Summary:\n{economic_summary}"

        prompt = f"""
        You are a senior researcher. Based on the following summaries,
        provide a concise, professional report highlighting key insights,
        trends, risks, and potential opportunities for {query}.
        {raw_combined_text}
        """
        kwargs = {"agent_name": self.name, "context": "research_stock"}
        final_summary = self.process(prompt, **kwargs)

        logger.info("--- Senior Researcher Final Summary for query '%s' ---", query)
        return final_summary

    def run_task(self, input_data: str) -> str:
        return self.research_stock(input_data)


# --- Child Agents ---
class StockAgent(Agent):
    def __init__(self):
        super().__init__("StockAgent", "stock data analyst", "mock")
        self.tool = stock_tool.StockTool()

    def fetch_and_summarize(
        self, symbol: str, period: str = "1mo", interval: str = "1d"
    ) -> str:
        logger.info("Fetching stock data for symbol: %s", symbol)
        try:
            history = self.tool.fetch_historical_data(
                symbol, period=period, interval=interval
            )
            history_text = ", ".join(
                f"{d}: {c}"
                for d, c in zip(
                    list(history["Close"].keys())[-10:],
                    list(history["Close"].values())[-10:],
                )
            )
            financials = self.tool.fetch_financial_info(symbol)
            info = self.tool.fetch_symbol_info(symbol)
            financial_summary = f"Market Cap: {info.get('market_cap')}, PE: {info.get('pe_ratio')}, Dividend Yield: {info.get('dividend_yield')}"
            prompt = f"""
            You are a stock data analyst. Summarize the stock performance for {symbol} based on:
            Recent closes: {history_text}
            Financial metrics: {financial_summary}
            """
            kwargs = {"agent_name": self.name, "context": "fetch_and_summarize"}
            summary_text = self.process(prompt, **kwargs)
            return summary_text
        except Exception as e:
            logger.exception("Error fetching/summarizing data for %s: %s", symbol, e)
            return f"Error fetching/summarizing data for {symbol}: {e}"

    def run_task(self, input_data: str) -> str:
        return self.fetch_and_summarize(input_data)


class NewsAgent(Agent):
    def __init__(self):
        super().__init__("NewsAgent", "financial news analyst", "mock")
        self.tool = news_tool.NewsTool()

    def select_news_source(self, query: str) -> str:
        prompt = f"""
        You are a financial news analyst. Decide the best news source for this query: {query}.
        Options: recent, history, db. Return one word.
        """
        kwargs = {"agent_name": self.name, "context": "select_news_source"}
        choice = self.process(prompt, **kwargs).strip().lower()
        if choice not in ["recent", "history", "db"]:
            choice = "recent"
        logger.info("Selected news source for query '%s': %s", query, choice)
        return choice

    def fetch_and_summarize(self, query: str, **kwargs) -> str:
        source = self.select_news_source(query)
        if "q" not in kwargs:
            kwargs["q"] = query
        articles = self.tool.fetch_news(source=source, **kwargs)
        raw_text = ""
        for a in articles[:10]:
            raw_text += f"Title: {a.title}\nDescription: {a.description}\nPublished: {a.publishedAt}\n\n"

        prompt = f"""
        You are a financial news sentiment analyst.
        Analyze the sentiment of the following news articles for the company/query '{query}'.
        Provide a concise summary of overall sentiment (positive, negative, neutral),
        highlight key drivers, and include examples from the articles:
        {raw_text}
        """
        kwargs = {"agent_name": self.name, "context": "fetch_and_analyze_sentiment"}
        sentiment_summary = self.process(prompt, **kwargs)
        logger.info("Sentiment analysis complete for query '%s'", query)
        return sentiment_summary

    def run_task(self, input_data: str) -> str:
        return self.fetch_and_summarize(input_data)


class EconomicAgent(Agent):
    def __init__(self):
        super().__init__("EconomicAgent", "economic data analyst", "mock")
        self.tool = economic_tool.EconomicDataTool()

    def fetch_and_summarize(
        self, series_ids: list, start_date: str = None, end_date: str = None
    ) -> str:
        raw_text = ""
        for series in series_ids:
            try:
                observations = self.tool.fetch_series(series, start_date, end_date)
                if observations:
                    obs_text = ", ".join(
                        f"{obs['date']}:{obs['value']}" for obs in observations[-10:]
                    )
                    raw_text += f"{series}: {obs_text}\n"
            except Exception as e:
                logger.exception("Error fetching economic data for %s: %s", series, e)
                raw_text += f"{series}: Error fetching data\n"

        prompt = f"""
        You are an economic data analyst. Summarize this economic data in a concise, professional format:
        {raw_text}
        """
        summary_text = self.process(prompt)
        logger.info("Economic summarization complete for series: %s", series_ids)
        return summary_text

    def run_task(self, input_data) -> str:
        series_ids = input_data if isinstance(input_data, list) else [input_data]
        return self.fetch_and_summarize(series_ids)
