from dotenv import load_dotenv
import yfinance as yf
from pydantic_ai import Agent
from models.stock_overview import StockOverview
from pydantic_ai.settings import ModelSettings

load_dotenv()

overview_agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    output_type=StockOverview,
    model_settings=ModelSettings(
        temperature=0.0
    ),
    system_prompt="""
    You are a stock research analyst.

    Given company information:

    1. Extract stock name.
    2. Extract sector.
    3. Extract industry.
    4. Summarize the business description in 2-3 lines.
    5. Return a valid StockOverview object.

    Note:
    -Use ONLY the information provided by the tool
    """
)


@overview_agent.tool_plain
def get_company_info(ticker: str) -> dict:
    """
    Fetch company information from Yahoo Finance.
    """

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "stock_name": info.get("longName", ticker),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "description": info.get(
            "longBusinessSummary",
            "No description available."
        )
    }

