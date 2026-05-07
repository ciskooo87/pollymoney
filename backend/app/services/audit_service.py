from __future__ import annotations

import json
import time
from uuid import uuid4

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.audit import AuditLog


class AuditService:
    def log(self, event_type: str, entity_type: str, message: str, entity_id: str | None = None, payload: dict | list | None = None) -> dict:
        record_id = str(uuid4())
        record = AuditLog(
            id=record_id,
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            message=message,
            payload_json=json.dumps(payload) if payload is not None else None,
            created_ts=int(time.time()),
        )
        with SessionLocal() as session:
            session.add(record)
            session.commit()
        return {"id": record_id, "event_type": event_type, "entity_type": entity_type}

    def recent(self, limit: int = 50, event_type: str | None = None) -> list[dict]:
        with SessionLocal() as session:
            stmt = select(AuditLog).order_by(AuditLog.created_ts.desc()).limit(limit)
            if event_type:
                stmt = select(AuditLog).where(AuditLog.event_type == event_type).order_by(AuditLog.created_ts.desc()).limit(limit)
            rows = session.execute(stmt).scalars().all()
            return [
                {
                    "id": row.id,
                    "event_type": row.event_type,
                    "entity_type": row.entity_type,
                    "entity_id": row.entity_id,
                    "message": row.message,
                    "payload_json": row.payload_json,
                    "created_ts": row.created_ts,
                }
                for row in rows
            ]

    def replay_for_trade(self, trade_id: str) -> list[dict]:
        with SessionLocal() as session:
            rows = session.execute(
                select(AuditLog)
                .where(AuditLog.entity_type == "trade", AuditLog.entity_id == trade_id)
                .order_by(AuditLog.created_ts.asc())
            ).scalars().all()
            return [
                {
                    "id": row.id,
                    "event_type": row.event_type,
                    "message": row.message,
                    "payload_json": row.payload_json,
                    "created_ts": row.created_ts,
                }
                for row in rows
            ]
