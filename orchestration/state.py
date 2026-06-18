from pydantic import BaseModel
from typing import Optional

from models.stock_overview import StockOverview
from models.sentiment import SentimentAnalysis
from models.stock_news import StockNews
from models.stock_technical import Technical
from models.stock_metrics import CurrentMetrics
from models.stock_risk import StockRisk
from models.stock_recommendation import StockRecommendation

class TradingState(BaseModel):

    user_query:str

    stock_name:str = None

    yfinance_symbol:str = None
    
    overview: Optional[StockOverview] = None

    current_metrics: Optional[CurrentMetrics] = None

    technical_analysis: Optional[Technical] = None

    news_analysis: Optional[StockNews] = None
    
    sentiment_analysis: Optional[SentimentAnalysis] = None
    
    risk_analysis: Optional[StockRisk] = None
    
    recommendation_analysis: Optional[StockRecommendation] = None