from typing import Any

from pydantic import BaseModel, Field


class TokenSnapshot(BaseModel):
    token_id: str
    outcome: str | None = None
    price: float | None = None
    winner: bool | None = None


class SimplifiedMarketSnapshot(BaseModel):
    condition_id: str
    active: bool
    closed: bool
    archived: bool
    accepting_orders: bool
    tokens: list[TokenSnapshot] = Field(default_factory=list)
    rewards: dict[str, Any] | None = None


class OrderLevel(BaseModel):
    price: str
    size: str


class OrderBookSnapshot(BaseModel):
    market: str
    asset_id: str
    timestamp: str
    hash: str
    bids: list[OrderLevel] = Field(default_factory=list)
    asks: list[OrderLevel] = Field(default_factory=list)
    min_order_size: str | None = None
    tick_size: str | None = None
    neg_risk: bool | None = None
    last_trade_price: str | None = None


class PricePoint(BaseModel):
    t: int
    p: float


class PriceHistoryResponse(BaseModel):
    history: list[PricePoint] = Field(default_factory=list)


class MarketSubscriptionRequest(BaseModel):
    asset_ids: list[str]
    level: int = 2
    initial_dump: bool = True
    custom_feature_enabled: bool = True


class UserSubscriptionRequest(BaseModel):
    markets: list[str] = Field(default_factory=list)


class WebsocketStatus(BaseModel):
    market_connected: bool
    user_connected: bool
    subscribed_assets: list[str] = Field(default_factory=list)
    subscribed_markets: list[str] = Field(default_factory=list)
    market_events_cached: int = 0
    user_events_cached: int = 0
