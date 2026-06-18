from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai import ModelSettings

load_dotenv()

stock_identify_agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    model_settings=ModelSettings(
        temperature=0.2
    ),
    system_prompt="""
    You are a stock identification agent.

    Your only task is to extract the company/stock name from the user's query.

    Rules:
    - Return ONLY the stock/company name.
    - Do not add explanations.
    - Do not add labels.
    - Do not add punctuation.
    - Do not return sentences.
    - If no stock/company name is present, return NONE.
    - Never guess a company name.

    Examples:

    User: Analyze TCS
    Output: Tata Consultancy Services

    User: Should I buy Infosys?
    Output: Infosys Ltd

    User: Give me a report on Reliance 
    Output: Reliance Industries Ltd

    User: Analyze Apple stock
    Output: Apple Inc

    User: What is the best stock to buy?
    Output: NONE

    User: How is the market today?
    Output: NONE
    """
)



