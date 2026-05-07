from fastapi import APIRouter

from app.schemas.order import OrderRequest
from app.services.execution import ExecutionService
from app.services.paper_trading import PaperTradingEngine
from app.services.audit_service import AuditService

router = APIRouter()
service = ExecutionService()
paper_engine = PaperTradingEngine()
audit_service = AuditService()


@router.post("/simulate")
def simulate_order(payload: OrderRequest):
    return service.submit_order(payload)


@router.post("/paper/run-cycle")
def run_paper_cycle(max_new_trades: int = 5):
    return paper_engine.run_cycle(max_new_trades=max_new_trades)


@router.get("/paper/summary")
def paper_summary():
    return paper_engine.summary()


@router.get("/paper/trades")
def paper_trades(limit: int = 20):
    return paper_engine.recent_trades(limit=limit)


@router.get("/paper/replay/{trade_id}")
def paper_trade_replay(trade_id: str):
    return audit_service.replay_for_trade(trade_id)


@router.get("/paper/audit")
def paper_audit(limit: int = 50, event_type: str | None = None):
    return audit_service.recent(limit=limit, event_type=event_type)
