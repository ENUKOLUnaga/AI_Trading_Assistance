from pydantic import BaseModel


class StockRisk(BaseModel):

    market_risk: str
    financial_risk: str
    technical_risk: str
    news_risk: str
    overall_risk_score: float