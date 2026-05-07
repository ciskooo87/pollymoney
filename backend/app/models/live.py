from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class LiveOrderRequest(Base):
    __tablename__ = "live_order_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    market_id: Mapped[str] = mapped_column(String, index=True)
    asset_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    strategy: Mapped[str] = mapped_column(String, index=True)
    side: Mapped[str] = mapped_column(String)
    size: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, index=True, default="pending_approval")
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    approved_by: Mapped[str | None] = mapped_column(String, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_ts: Mapped[int] = mapped_column(Integer, index=True)
    decided_ts: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)


class LiveExecutionConfig(Base):
    __tablename__ = "live_execution_config"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    wallet_address: Mapped[str | None] = mapped_column(String, nullable=True)
    clob_api_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    clob_api_secret: Mapped[str | None] = mapped_column(Text, nullable=True)
    clob_api_passphrase: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    armed_for_execution: Mapped[bool] = mapped_column(Boolean, default=False)
    require_human_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    max_live_notional: Mapped[float] = mapped_column(Float, default=100.0)
    signature_type: Mapped[int] = mapped_column(Integer, default=1)
    funder_address: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_ts: Mapped[int | None] = mapped_column(Integer, nullable=True)
