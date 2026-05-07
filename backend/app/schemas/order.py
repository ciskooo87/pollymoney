from pydantic import BaseModel, Field

class OrderRequest(BaseModel):
    market_id: str
    strategy: str
    side: str
    price: float = Field(gt=0, lt=1)
    size: float = Field(gt=0)
    expected_edge: float
    confidence: float = Field(ge=0, le=1)
