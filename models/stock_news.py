from pydantic import BaseModel
from typing import List

class StockNews(BaseModel):
    
    positive_news:List[str]
    negative_news:List[str]
    overall_sentiment:str
    overall_score:float