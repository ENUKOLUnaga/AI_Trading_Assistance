from pydantic import BaseModel
from typing import List


class StockRecommendation(BaseModel):

    recommendation: str
    confidence_score: float
    investment_horizon: str
    reasons: List[str]