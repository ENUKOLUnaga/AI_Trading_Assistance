import yfinance as yf
import pandas_ta as ta
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai import ModelSettings


from models.stock_technical import Technical

load_dotenv()

technical_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    output_type=Technical,
    model_settings=ModelSettings(
        temperature=0.0
    ),
    system_prompt=
    """
    You are a professional stock market technical analyst.

    Analyze ONLY the technical indicators provided by the tool.

    Available Indicators:

    * Current Price
    * RSI
    * MACD
    * Signal Line
    * 50-Day Moving Average
    * 200-Day Moving Average
    * Current Volume
    * Average Volume

    Determine:

    1. Trend

    * Bullish
    * Bearish
    * Neutral

    Trend Rules:

    * Bullish: Current Price > MA50 and MA50 > MA200
    * Bearish: Current Price < MA50 and MA50 < MA200
    * Neutral: Any mixed condition

    2. RSI Signal

    * Bullish: RSI > 60
    * Neutral: RSI between 40 and 60
    * Bearish: RSI < 40

    3. MACD Signal

    * Bullish: MACD > Signal Line
    * Bearish: MACD < Signal Line
    * Neutral: Difference is negligible

    4. Volume Trend

    * High Volume: Current Volume > Average Volume × 1.2
    * Average Volume: Current Volume within ±20% of Average Volume
    * Low Volume: Current Volume < Average Volume × 0.8

    5. Momentum

    * Positive: RSI Bullish and MACD Bullish
    * Negative: RSI Bearish and MACD Bearish
    * Neutral: Mixed signals

    6. Technical Summary

    * Summarize the overall technical outlook in 2-3 concise sentences.

    Critical Guardrails:

    * Use ONLY the supplied indicator values.
    * Do NOT invent values.
    * Do NOT use external market knowledge.
    * Do NOT predict future stock prices.
    * Do NOT assume future trends.
    * If any indicator is missing, mention insufficient data.
    * Ensure all conclusions are consistent with the provided indicators.

    Return only a valid Technical object.
    """
    )

@technical_agent.tool_plain
def technical_analysis(ticker: str)-> dict:

    stock = yf.Ticker(ticker)

    df = stock.history(period="1y")

    close = df["Close"]
    volume = df["Volume"]

    #Calculating RSI
    df["RSI"] = ta.rsi(
        close,
        length=14
    )

    rsi = float(df["RSI"].iloc[-1])

    #calculating MACD
    macd = ta.macd(close)

    macd_value = float(
        macd["MACD_12_26_9"].iloc[-1]
    )

    signal_value = float(
        macd["MACDs_12_26_9"].iloc[-1]
    )
    
    #moving Averages
    ma50 = float(
        close.rolling(50).mean().iloc[-1]
    )

    ma200 = float(
        close.rolling(200).mean().iloc[-1]
    )

    current_price = float(
        close.iloc[-1]
    )

    #volume Trend
    avg_volume = volume.tail(20).mean()

    current_volume = volume.iloc[-1]

    return {
        "Current Price": float(current_price),
        "RSI": float(rsi),
        "MACD": float(macd_value),
        "Signal Line": float(signal_value),
        "50 Day Moving Average": float(ma50),
        "200 Day Moving Average": float(ma200),
        "Current Volume": int(current_volume),
        "Average Volume": float(avg_volume)
    }
