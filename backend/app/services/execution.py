from uuid import uuid4

from app.core.config import settings
from app.schemas.order import OrderRequest


class ExecutionService:
    def submit_order(self, payload: OrderRequest) -> dict:
        mode = "live" if settings.enable_live_trading else "paper"
        accepted = mode == "paper"
        rationale = (
            "Ordem aceita para simulação paper." if mode == "paper"
            else "Runtime de live execution existe, mas envio real deve passar pelo fluxo controlado /orders/live/request."
        )
        return {
            "order_id": str(uuid4()),
            "mode": mode,
            "accepted": accepted,
            "human_approval_required": settings.require_human_approval,
            "payload": payload.model_dump(),
            "rationale": rationale,
        }
