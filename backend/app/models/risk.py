from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class RiskState(Base):
    __tablename__ = "risk_state"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    trading_day: Mapped[str] = mapped_column(String, index=True)
    paused: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    pause_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    daily_profit_target: Mapped[float] = mapped_column(Float, default=200.0)
    daily_loss_limit: Mapped[float] = mapped_column(Float, default=-150.0)
    max_drawdown_limit: Mapped[float] = mapped_column(Float, default=-600.0)
    current_realized_pnl: Mapped[float] = mapped_column(Float, default=0.0)
    current_unrealized_pnl: Mapped[float] = mapped_column(Float, default=0.0)
    loss_streak: Mapped[int] = mapped_column(Integer, default=0)
    max_concurrent_positions: Mapped[int] = mapped_column(Integer, default=12)
    max_position_size: Mapped[float] = mapped_column(Float, default=400.0)
    updated_ts: Mapped[int | None] = mapped_column(Integer, nullable=True)
