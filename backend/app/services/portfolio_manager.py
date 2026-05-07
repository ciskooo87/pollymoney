from __future__ import annotations

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.trade import Trade


class PortfolioManager:
    def snapshot(self) -> dict:
        with SessionLocal() as session:
            open_positions = session.execute(
                select(Trade).where(Trade.paper.is_(True), Trade.status == "open")
            ).scalars().all()
            closed_positions = session.execute(
                select(Trade).where(Trade.paper.is_(True), Trade.status == "closed")
            ).scalars().all()
            realized = session.scalar(
                select(func.coalesce(func.sum(Trade.realized_pnl), 0.0)).where(Trade.paper.is_(True), Trade.status == "closed")
            ) or 0.0
            exposure = sum(abs(t.price * t.size) for t in open_positions)
            by_strategy: dict[str, float] = {}
            for trade in open_positions:
                by_strategy[trade.strategy] = by_strategy.get(trade.strategy, 0.0) + abs(trade.price * trade.size)
            return {
                "open_positions": len(open_positions),
                "closed_positions": len(closed_positions),
                "gross_exposure": round(exposure, 2),
                "realized_pnl": float(realized),
                "exposure_by_strategy": [
                    {"strategy": key, "exposure": round(value, 2)}
                    for key, value in sorted(by_strategy.items(), key=lambda item: item[1], reverse=True)
                ],
            }
