from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    market_id: Mapped[str] = mapped_column(String, index=True)
    asset_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    strategy: Mapped[str] = mapped_column(String, index=True)
    side: Mapped[str] = mapped_column(String)
    size: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    expected_edge: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="simulated", index=True)
    paper: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    rationale: Mapped[str | None] = mapped_column(String, nullable=True)
    opened_ts: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    closed_ts: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    realized_pnl: Mapped[float | None] = mapped_column(Float, nullable=True)
