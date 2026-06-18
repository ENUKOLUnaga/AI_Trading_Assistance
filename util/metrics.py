from dotenv import load_dotenv
import yfinance as yf
from models.stock_metrics import CurrentMetrics

load_dotenv()

def stock_metrics(ticker: str):

    stock = yf.Ticker(ticker)
    info = stock.info

    metrics = CurrentMetrics(
        current_price=info.get("currentPrice", 0),
        market_cap = info.get("marketCap", 0),
        pe_ratio=info.get("trailingPE",0),
        eps=info.get("trailingEps", 0),
        dividend_yield=info.get("dividendYield", 0),
        revenue_growth=info.get("revenueGrowth", 0),
        profit_margin=info.get("profitMargins",  0),
        debt_to_equity=info.get("debtToEquity", 0)
    )

    return metrics
