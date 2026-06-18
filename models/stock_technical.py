from pydantic import BaseModel

class Technical(BaseModel):
    
    trend: str
    rsi: float
    macd_signal: str
    moving_average_50: float
    moving_average_200: float
    volume_trend: str
    momentum: str
    technical_summary: str