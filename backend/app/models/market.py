from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Market(Base):
    __tablename__ = "markets"

    condition_id: Mapped[str] = mapped_column(String, primary_key=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    closed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    archived: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    accepting_orders: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    reward_min_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    reward_max_spread: Mapped[float | None] = mapped_column(Float, nullable=True)


class MarketToken(Base):
    __tablename__ = "market_tokens"

    token_id: Mapped[str] = mapped_column(String, primary_key=True)
    condition_id: Mapped[str] = mapped_column(String, index=True)
    outcome: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    winner: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class MarketOrderBook(Base):
    __tablename__ = "market_order_books"

    asset_id: Mapped[str] = mapped_column(String, primary_key=True)
    condition_id: Mapped[str] = mapped_column(String, index=True)
    book_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    timestamp: Mapped[str | None] = mapped_column(String, nullable=True)
    best_bid: Mapped[float | None] = mapped_column(Float, nullable=True)
    best_ask: Mapped[float | None] = mapped_column(Float, nullable=True)
    bid_depth: Mapped[int] = mapped_column(Integer, default=0)
    ask_depth: Mapped[int] = mapped_column(Integer, default=0)
    last_trade_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    tick_size: Mapped[str | None] = mapped_column(String, nullable=True)
    min_order_size: Mapped[str | None] = mapped_column(String, nullable=True)
    neg_risk: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    raw_bids: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_asks: Mapped[str | None] = mapped_column(Text, nullable=True)


class MarketPriceHistoryPoint(Base):
    __tablename__ = "market_price_history"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    asset_id: Mapped[str] = mapped_column(String, index=True)
    ts: Mapped[int] = mapped_column(Integer, index=True)
    price: Mapped[float] = mapped_column(Float)
    interval: Mapped[str | None] = mapped_column(String, nullable=True)
    fidelity: Mapped[int | None] = mapped_column(Integer, nullable=True)
