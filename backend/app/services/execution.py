from uuid import uuid4

from app.core.config import settings
from app.schemas.order import OrderRequest

class ExecutionService:
    def submit_order(self, payload: OrderRequest) -> dict:
        mode = "live" if settings.enable_live_trading else "paper"
        return {
            "order_id": str(uuid4()),
            "mode": mode,
            "accepted": True,
            "human_approval_required": settings.require_human_approval,
            "payload": payload.model_dump(),
            "rationale": "Ordem aceita pelo execution gateway e marcada para simulação padrão.",
        }
