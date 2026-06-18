from pydantic import BaseModel


class CurrentMetrics(BaseModel):

    current_price: float
    market_cap: float
    pe_ratio: float
    eps: float
    dividend_yield: float
    revenue_growth: float
    profit_margin: float
    debt_to_equity: float