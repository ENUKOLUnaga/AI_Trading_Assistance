import streamlit as st
import requests
from datetime import datetime

API_URL = "https://ai-trading-assistance.onrender.com/analyze"

st.set_page_config(
    page_title="AI Trading Assistant",
    layout="wide"
)

st.title("📈 AI Trading Assistant")

# Disclaimer Guardrail
st.warning(
    """
    ⚠️ This analysis is AI-generated and intended for educational purposes only.

    It is NOT financial advice. Please conduct your own research
    before making investment decisions.
    """
)

agree = st.checkbox(
    "I understand this is not financial advice."
)

user_query = st.text_input(
    "Enter Stock Query",
    placeholder="Analyze TCS"
)

if st.button("Analyze"):

    # Input Validation Guardrail
    if not agree:
        st.warning(
            "Please acknowledge the disclaimer before continuing."
        )
        st.stop()

    if not user_query.strip():
        st.error(
            "Please enter a stock query."
        )
        st.stop()

    try:
        # Loading Spinner
        with st.spinner("Analyzing stock..."):

            response = requests.get(
                API_URL,
                params={"user_query": user_query},
                timeout=120
            )

    except requests.exceptions.Timeout:

        st.error(
            "Analysis timed out."
        )
        st.stop()

    except Exception as e:

        st.error(
            f"Connection Error: {e}"
        )
        st.stop()

    if response.status_code != 200:

        try:
            error_message = response.json().get(
                "detail",
                "Unknown Error"
            )
            
        except Exception:
            error_message = "Unknown Error"

        if response.status_code == 401:
            st.error(f"🔑 {error_message}")

        elif response.status_code == 429:
            st.warning(f"⏳ {error_message}")

        else:
            st.error(error_message)

        st.stop()

    try:
        result = response.json()
    except Exception:
        st.error("Invalid response received from server.")
        st.stop()

    # Required Sections Guardrail
    required_sections = [
        "overview",
        "current_metrics",
        "technical_analysis",
        "news_analysis",
        "sentiment_analysis",
        "risk_analysis",
        "recommendation_analysis"
    ]

    for section in required_sections:
        if section not in result:
            st.error(f"Missing analysis section: {section}")
            st.stop()

    # Timestamp
    st.caption(
        f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    # Header
    st.header(result.get("stock_name", "Unknown Stock"))

    recommendation = result.get("recommendation_analysis", {})
    confidence = recommendation.get("confidence_score", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Symbol",result["yfinance_symbol"])

    with col2:
        st.metric("Recommendation",recommendation["recommendation"])

    with col3:
        st.metric("Confidence",f"{confidence}%")

    # Confidence 
    if confidence < 50:
        st.warning(
            "⚠️ Low confidence recommendation. Additional research is recommended."
        )

    # Company Overview
    st.subheader("🏢 Company Overview")
    overview = result["overview"]

    st.write("Sector:", overview["sector"])
    st.write("Industry:", overview["industry"])
    st.write(overview["company_overview"])

    # Current Metrics
    st.subheader("📊 Current Metrics")
    metrics = result["current_metrics"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Price", f"₹{metrics['current_price']}")
    c2.metric("PE Ratio", metrics["pe_ratio"])
    c3.metric("EPS", metrics["eps"])

    c4, c5, c6 = st.columns(3)
    c4.metric(
        "Revenue Growth",
        f"{metrics['revenue_growth']*100:.2f}%"
    )
    c5.metric(
        "Profit Margin",
        f"{metrics['profit_margin']*100:.2f}%"
    )
    c6.metric(
        "Debt To Equity",
        metrics["debt_to_equity"]
    )

    # Technical Analysis
    st.subheader("📈 Technical Analysis")
    technical = result["technical_analysis"]

    st.write("Trend:", technical["trend"])
    st.write("RSI:", technical["rsi"])
    st.write("MACD Signal:", technical["macd_signal"])
    st.write("50 DMA:", technical["moving_average_50"])
    st.write("200 DMA:", technical["moving_average_200"])
    st.write("Volume Trend:", technical["volume_trend"])
    st.write("Momentum:", technical["momentum"])
    st.info(technical["technical_summary"])

    # News Analysis
    st.subheader("📰 News Analysis")
    news = result["news_analysis"]

    st.write(
        "Overall Sentiment:",
        news["overall_sentiment"]
    )
    st.write(
        "Sentiment Score:",
        news["overall_score"]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.success("Positive News")
        positive_news = news.get("positive_news", [])

        if positive_news:
            for item in positive_news:
                st.write("•", item)
        else:
            st.write("No positive news found.")

    with col2:
        st.error("Negative News")
        negative_news = news.get("negative_news", [])
        
        if negative_news:
            for item in negative_news:
                st.write("•", item)
        else:
            st.write("No negative news found.")

    # Sentiment Analysis
    st.subheader("😊 Sentiment Analysis")
    sentiment = result["sentiment_analysis"]

    st.write(
        "Sentiment:",
        sentiment["sentiment"]
    )
    st.write(
        "Confidence:",
        sentiment["confidence"]
    )

    if sentiment["positive_factors"]:
        st.write("### Positive Factors")
        for item in sentiment["positive_factors"]:
            st.write("✅", item)

    if sentiment["negative_factors"]:
        st.write("### Negative Factors")
        for item in sentiment["negative_factors"]:
            st.write("❌", item)

    st.info(
        sentiment["summary"]
    )

    # Risk Analysis
    st.subheader("⚠️ Risk Analysis")
    risk = result["risk_analysis"]

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Market Risk", risk["market_risk"])
    r2.metric("Financial Risk", risk["financial_risk"])
    r3.metric("Technical Risk", risk["technical_risk"])
    r4.metric("News Risk", risk["news_risk"])

    st.write(
        "Overall Risk Score:",
        risk["overall_risk_score"]
    )

    # Risk Guardrail
    if risk["overall_risk_score"] >= 7:
        st.error("🚨 High Risk Stock Detected")

    elif risk["overall_risk_score"] >= 4:
        st.warning("⚠️ Medium Risk Stock")

    else:
        st.success("✅ Low Risk Stock")

    # Final Recommendation
    st.subheader("🎯 Final Recommendation")

    if recommendation["recommendation"] == "BUY":
        st.success(f"BUY ({confidence}%)")

    elif recommendation["recommendation"] == "HOLD":
        st.warning(f"HOLD ({confidence}%)")

    else:
        st.error(f"SELL ({confidence}%)")

    # Recommendation Consistency
    if (
        recommendation["recommendation"] == "BUY"
        and risk["overall_risk_score"] >= 7
    ):
        st.error(
            "Guardrail Alert: BUY recommendation conflicts with High Risk assessment."
        )

    st.write(
        "Investment Horizon:",
        recommendation["investment_horizon"]
    )

    st.write("### Reasons")

    for reason in recommendation["reasons"]:
        st.write("•", reason)

    # Hallucination Warning
    st.info(
        """
        AI recommendations are generated using available
        financial, technical, news, and sentiment data.

        Market conditions can change rapidly.
        Always perform independent research before investing.
        """
    )