import yfinance as yf

def find_ticker(stock_name: str):

    search = yf.Search(stock_name)
    quotes = search.quotes
    if not quotes:
        raise ValueError(
            f"No stock found for {stock_name}"
        )

    return quotes[0]["symbol"]