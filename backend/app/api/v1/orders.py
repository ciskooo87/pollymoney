from fastapi import APIRouter

from app.schemas.live import LiveArmRequest, LiveExecutionConfigRequest, LiveOrderDecisionRequest
from app.schemas.order import OrderRequest
from app.services.ai_repository import AIRepository
from app.services.audit_service import AuditService
from app.services.execution import ExecutionService
from app.services.live_execution import LiveExecutionService
from app.services.paper_trading import PaperTradingEngine

router = APIRouter()
service = ExecutionService()
paper_engine = PaperTradingEngine()
audit_service = AuditService()
ai_repository = AIRepository()
live_service = LiveExecutionService()


@router.post("/simulate")
def simulate_order(payload: OrderRequest):
    return service.submit_order(payload)


@router.post("/live/request")
def request_live_order(payload: OrderRequest):
    return live_service.submit_live_order(payload)


@router.get("/live/requests")
def live_requests(limit: int = 50):
    return live_service.list_requests(limit=limit)


@router.post("/live/requests/{request_id}/decision")
def decide_live_request(request_id: str, payload: LiveOrderDecisionRequest):
    return live_service.decide_request(request_id, payload)


@router.get("/live/config")
def live_config():
    return live_service.get_config()


@router.post("/live/config")
def update_live_config(payload: LiveExecutionConfigRequest):
    return live_service.update_config(payload)


@router.post("/live/arm")
def arm_live_execution(payload: LiveArmRequest):
    return live_service.set_arm_state(payload)


@router.get("/live/wallet-status")
def live_wallet_status():
    return live_service.wallet_status()


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


@router.get("/paper/ai-decisions")
def paper_ai_decisions(limit: int = 20):
    return ai_repository.recent(limit=limit)
