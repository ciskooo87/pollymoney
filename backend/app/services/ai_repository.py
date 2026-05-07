from __future__ import annotations

import json
import time
from uuid import uuid4

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.ai_decision import AIDecision


class AIRepository:
    def create_decision(self, trade_id: str | None, market_id: str, asset_id: str | None, strategy: str, decision: dict) -> dict:
        record_id = str(uuid4())
        record = AIDecision(
            id=record_id,
            trade_id=trade_id,
            market_id=market_id,
            asset_id=asset_id,
            strategy=strategy,
            confidence_score=float(decision["confidence_score"]),
            probability_estimate=float(decision["probability_estimate"]),
            expected_edge=float(decision["expected_edge"]),
            risk_classification=decision["risk_classification"],
            trade_rank_score=float(decision["trade_rank_score"]),
            justification=decision["justification"],
            features_json=json.dumps(decision.get("features", {})),
            created_ts=int(time.time()),
        )
        with SessionLocal() as session:
            session.add(record)
            session.commit()
        return {"id": record_id, "trade_id": trade_id, "market_id": market_id}

    def attach_trade(self, decision_id: str, trade_id: str) -> None:
        with SessionLocal() as session:
            record = session.get(AIDecision, decision_id)
            if record is None:
                return
            record.trade_id = trade_id
            session.commit()

    def recent(self, limit: int = 20) -> list[dict]:
        with SessionLocal() as session:
            rows = session.execute(select(AIDecision).order_by(AIDecision.created_ts.desc()).limit(limit)).scalars().all()
            return [
                {
                    "id": row.id,
                    "trade_id": row.trade_id,
                    "market_id": row.market_id,
                    "asset_id": row.asset_id,
                    "strategy": row.strategy,
                    "confidence_score": row.confidence_score,
                    "probability_estimate": row.probability_estimate,
                    "expected_edge": row.expected_edge,
                    "risk_classification": row.risk_classification,
                    "trade_rank_score": row.trade_rank_score,
                    "justification": row.justification,
                    "features_json": row.features_json,
                    "created_ts": row.created_ts,
                }
                for row in rows
            ]

    def by_trade(self, trade_id: str) -> list[dict]:
        with SessionLocal() as session:
            rows = session.execute(
                select(AIDecision).where(AIDecision.trade_id == trade_id).order_by(AIDecision.created_ts.asc())
            ).scalars().all()
            return [
                {
                    "id": row.id,
                    "trade_id": row.trade_id,
                    "market_id": row.market_id,
                    "strategy": row.strategy,
                    "confidence_score": row.confidence_score,
                    "probability_estimate": row.probability_estimate,
                    "expected_edge": row.expected_edge,
                    "risk_classification": row.risk_classification,
                    "trade_rank_score": row.trade_rank_score,
                    "justification": row.justification,
                    "features_json": row.features_json,
                    "created_ts": row.created_ts,
                }
                for row in rows
            ]
