from fastapi import FastAPI
from pydantic import BaseModel
from orchestration.orchestration import run_trading_assistant

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str

@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/analyze")
async def analyze(user_query: str):
    try:
        result = await run_trading_assistant(user_query)
        return result.model_dump()
    except Exception as e:
        return {"error": str(e)}