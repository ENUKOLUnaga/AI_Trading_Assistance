import asyncio

from agents.news_agent import news_agent
from agents.overview_agent import overview_agent
from agents.stock_identify_agent import stock_identify_agent
from agents.technical_agent import technical_agent
from agents.sentiment_agent import sentiment_agent
from agents.risk_analysis import risk_agent
from agents.recommendation_agent import recommendation_agent

from orchestration.state import TradingState
from util.symbol_resolver import find_ticker
from util.metrics import stock_metrics

async def run_trading_assistant(
    user_query: str
):
    state = TradingState(
        user_query=user_query
    )

    stock = await stock_identify_agent.run(
        state.user_query
    )

    state.stock_name = stock.output

    state.yfinance_symbol = find_ticker(
        state.stock_name
    )
    
    current_metrics = asyncio.to_thread(
        stock_metrics,
        state.yfinance_symbol
    )
    
    overview_task = overview_agent.run(
        state.yfinance_symbol
    )

    technical_task = technical_agent.run(
        state.yfinance_symbol
    )

    news_task = news_agent.run(
        state.yfinance_symbol
    )

    status = (
        await asyncio.gather(
            overview_task,
            technical_task,
            news_task, 
            current_metrics
        )
    )

    state.overview = (
        status[0].output
    )

    state.technical_analysis = (
        status[1].output
    )

    state.news_analysis = (
        status[2].output
    )
    
    state.current_metrics = status[3]
    
    sentiment_analysis = await sentiment_agent.run(
        state.model_dump_json()
    )
    
    state.sentiment_analysis = sentiment_analysis.output

    risk_analysis = await risk_agent.run(
        state.model_dump_json()
    )
    
    state.risk_analysis = risk_analysis.output
    
    recommendation = await recommendation_agent.run(
        state.model_dump_json()
    )
    
    state.recommendation_analysis = recommendation.output
    
    return state




