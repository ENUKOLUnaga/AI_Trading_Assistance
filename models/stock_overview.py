from pydantic import BaseModel, Field

class StockOverview(BaseModel):

    stock_name: str = Field(
        min_length=1,
        max_length=200
    )

    sector: str

    industry: str

    company_overview: str = Field(
        min_length=1,
        max_length=1000
    )