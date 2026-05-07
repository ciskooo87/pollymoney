from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AIDecision(Base):
    __tablename__ = "ai_decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    trade_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    market_id: Mapped[str] = mapped_column(String, index=True)
    asset_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    strategy: Mapped[str] = mapped_column(String, index=True)
    confidence_score: Mapped[float] = mapped_column(Float)
    probability_estimate: Mapped[float] = mapped_column(Float)
    expected_edge: Mapped[float] = mapped_column(Float)
    risk_classification: Mapped[str] = mapped_column(String, index=True)
    trade_rank_score: Mapped[float] = mapped_column(Float)
    justification: Mapped[str] = mapped_column(Text)
    features_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_ts: Mapped[int] = mapped_column(Integer, index=True)
