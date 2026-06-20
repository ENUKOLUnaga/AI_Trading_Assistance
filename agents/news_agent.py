from dotenv import load_dotenv
from pydantic_ai import Agent
import yfinance as yf
from models.stock_news import StockNews
from pydantic_ai.settings import ModelSettings

load_dotenv()

news_agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    output_type=StockNews,
    model_settings=ModelSettings(
        temperature=0.1
    ),
    system_prompt="""
    You are a professional financial news analyst.

    Analyze stock-related news headlines.

    Rules:

    - Do not invent news events.
    - Do not infer events that are not explicitly mentioned.
    - Every positive news item must be supported by a headline.
    - Every negative news item must be supported by a headline.
    - Do not use external knowledge.
    - Do not assume future outcomes.

    Sentiment must be:
    - Positive
    - Neutral
    - Negative

    Return ONLY structured output.
    """
)

@news_agent.tool_plain
def fetch_news(ticker: str):
    
    stock = yf.Ticker(ticker)

    if not stock.news:
        raise ValueError(
            f"No news available for {ticker}"
        )

    return stock.news[:10]

if __name__=="__main__":
    print(news_agent.run_sync("infy.NS"))
