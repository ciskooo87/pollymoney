from __future__ import annotations

import time
from uuid import uuid4

from sqlalchemy import select

from app.core.config import settings
from app.core.security import SecretBox
from app.db.session import SessionLocal
from app.models.live import LiveExecutionConfig, LiveOrderRequest
from app.schemas.live import LiveArmRequest, LiveExecutionConfigRequest, LiveOrderDecisionRequest
from app.schemas.order import OrderRequest
from app.services.ai_repository import AIRepository
from app.services.ai_service import AIService
from app.services.audit_service import AuditService


class LiveExecutionService:
    def __init__(self):
        self.audit = AuditService()
        self.ai = AIService()
        self.ai_repo = AIRepository()
        self.secret_box = SecretBox(settings.encryption_key)

    def get_config(self) -> dict:
        cfg = self._ensure_config()
        return self._serialize_config(cfg, redact=True)

    def update_config(self, payload: LiveExecutionConfigRequest) -> dict:
        now = int(time.time())
        with SessionLocal() as session:
            cfg = session.get(LiveExecutionConfig, "default")
            if cfg is None:
                cfg = LiveExecutionConfig(id="default")
                session.add(cfg)
            cfg.wallet_address = payload.wallet_address
            cfg.clob_api_key = self._enc(payload.clob_api_key)
            cfg.clob_api_secret = self._enc(payload.clob_api_secret)
            cfg.clob_api_passphrase = self._enc(payload.clob_api_passphrase)
            cfg.enabled = payload.enabled
            cfg.armed_for_execution = payload.armed_for_execution
            cfg.require_human_approval = payload.require_human_approval
            cfg.max_live_notional = payload.max_live_notional
            cfg.signature_type = payload.signature_type
            cfg.funder_address = payload.funder_address
            cfg.updated_ts = now
            session.commit()
            session.refresh(cfg)
        self.audit.log("live_config_updated", "live_config", "live execution config updated", entity_id="default", payload=self._serialize_config(cfg, redact=True))
        return self._serialize_config(cfg, redact=True)

    def set_arm_state(self, payload: LiveArmRequest) -> dict:
        with SessionLocal() as session:
            cfg = session.get(LiveExecutionConfig, "default")
            if cfg is None:
                cfg = LiveExecutionConfig(id="default", enabled=False, armed_for_execution=False, require_human_approval=True, max_live_notional=100.0, signature_type=1, updated_ts=int(time.time()))
                session.add(cfg)
            cfg.armed_for_execution = payload.armed
            cfg.updated_ts = int(time.time())
            session.commit()
            session.refresh(cfg)
        self.audit.log("live_arm_state_changed", "live_config", "live execution arm state changed", entity_id="default", payload={"armed": payload.armed, "changed_by": payload.changed_by, "reason": payload.reason})
        return self._serialize_config(cfg, redact=True)

    def submit_live_order(self, payload: OrderRequest) -> dict:
        cfg = self._ensure_config()
        ai_decision = self.ai.evaluate_trade(
            market_id=payload.market_id,
            asset_id=None,
            strategy=payload.strategy,
            price=payload.price,
            confidence=payload.confidence,
            edge=payload.expected_edge,
        )
        self.ai_repo.create_decision(None, payload.market_id, None, payload.strategy, ai_decision)
        if not settings.enable_live_trading or not cfg.enabled:
            status = "blocked_runtime_disabled"
        elif not cfg.armed_for_execution:
            status = "blocked_kill_switch"
        elif not self._has_credentials(cfg):
            status = "blocked_missing_credentials"
        elif (payload.price * payload.size) > cfg.max_live_notional:
            status = "blocked_notional_limit"
        else:
            status = "pending_approval" if cfg.require_human_approval or settings.require_human_approval else "approved_not_executed"

        req_id = str(uuid4())
        with SessionLocal() as session:
            row = LiveOrderRequest(
                id=req_id,
                market_id=payload.market_id,
                asset_id=None,
                strategy=payload.strategy,
                side=payload.side,
                size=payload.size,
                price=payload.price,
                status=status,
                rationale=ai_decision["justification"],
                approval_required=(cfg.require_human_approval or settings.require_human_approval),
                created_ts=int(time.time()),
            )
            session.add(row)
            session.commit()
        self.audit.log("live_order_requested", "live_order", "live order requested", entity_id=req_id, payload={"payload": payload.model_dump(), "status": status, "ai": ai_decision})
        return {"request_id": req_id, "status": status, "ai_decision": ai_decision, "live_enabled": settings.enable_live_trading and cfg.enabled, "armed": cfg.armed_for_execution}

    def list_requests(self, limit: int = 50) -> list[dict]:
        with SessionLocal() as session:
            rows = session.execute(select(LiveOrderRequest).order_by(LiveOrderRequest.created_ts.desc()).limit(limit)).scalars().all()
            return [self._serialize_request(row) for row in rows]

    def decide_request(self, request_id: str, payload: LiveOrderDecisionRequest) -> dict:
        with SessionLocal() as session:
            row = session.get(LiveOrderRequest, request_id)
            if row is None:
                return {"error": "request_not_found"}
            row.decided_ts = int(time.time())
            row.approved_by = payload.decided_by
            if payload.approved:
                row.status = "approved_not_executed"
            else:
                row.status = "rejected"
                row.rejection_reason = payload.rejection_reason or "rejected_by_operator"
            session.commit()
            session.refresh(row)
        self.audit.log("live_order_decided", "live_order", "live order approval decision recorded", entity_id=request_id, payload=self._serialize_request(row))
        return self._serialize_request(row)

    def wallet_status(self) -> dict:
        cfg = self._ensure_config()
        return {
            "wallet_address": cfg.wallet_address,
            "funder_address": cfg.funder_address,
            "signature_type": cfg.signature_type,
            "has_api_key": bool(cfg.clob_api_key),
            "has_api_secret": bool(cfg.clob_api_secret),
            "has_api_passphrase": bool(cfg.clob_api_passphrase),
            "has_encrypted_private_key": bool(settings.wallet_private_key_encrypted),
            "has_rpc_url": bool(settings.web3_rpc_url),
            "armed_for_execution": cfg.armed_for_execution,
            "runtime_live_enabled": settings.enable_live_trading,
        }

    def _ensure_config(self) -> LiveExecutionConfig:
        with SessionLocal() as session:
            cfg = session.get(LiveExecutionConfig, "default")
            if cfg is None:
                cfg = LiveExecutionConfig(id="default", enabled=False, armed_for_execution=False, require_human_approval=True, max_live_notional=100.0, signature_type=1, updated_ts=int(time.time()))
                session.add(cfg)
                session.commit()
                session.refresh(cfg)
            return cfg

    def _serialize_config(self, cfg: LiveExecutionConfig, redact: bool = False) -> dict:
        return {
            "wallet_address": cfg.wallet_address,
            "clob_api_key": "configured" if redact and cfg.clob_api_key else self._dec(cfg.clob_api_key),
            "clob_api_secret": "configured" if redact and cfg.clob_api_secret else self._dec(cfg.clob_api_secret),
            "clob_api_passphrase": "configured" if redact and cfg.clob_api_passphrase else self._dec(cfg.clob_api_passphrase),
            "enabled": cfg.enabled,
            "armed_for_execution": cfg.armed_for_execution,
            "require_human_approval": cfg.require_human_approval,
            "max_live_notional": cfg.max_live_notional,
            "signature_type": cfg.signature_type,
            "funder_address": cfg.funder_address,
            "updated_ts": cfg.updated_ts,
        }

    def _serialize_request(self, row: LiveOrderRequest) -> dict:
        return {
            "id": row.id,
            "market_id": row.market_id,
            "asset_id": row.asset_id,
            "strategy": row.strategy,
            "side": row.side,
            "size": row.size,
            "price": row.price,
            "status": row.status,
            "rationale": row.rationale,
            "approval_required": row.approval_required,
            "approved_by": row.approved_by,
            "rejection_reason": row.rejection_reason,
            "created_ts": row.created_ts,
            "decided_ts": row.decided_ts,
        }

    def _has_credentials(self, cfg: LiveExecutionConfig) -> bool:
        return bool(cfg.wallet_address and cfg.clob_api_key and cfg.clob_api_secret and cfg.clob_api_passphrase)

    def _enc(self, value: str | None) -> str | None:
        if not value:
            return None
        return self.secret_box.encrypt(value)

    def _dec(self, value: str | None) -> str | None:
        if not value:
            return None
        return self.secret_box.decrypt(value)
