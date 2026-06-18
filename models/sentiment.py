from pydantic import BaseModel

class SentimentAnalysis(BaseModel):

    sentiment: str
    confidence: float
    positive_factors: list[str]
    negative_factors: list[str]
    summary: str