from fastapi import APIRouter

from app.services.market_repository import MarketRepository
from app.services.paper_trading import PaperTradingEngine
from app.services.audit_service import AuditService
from app.services.ai_repository import AIRepository
from app.services.live_execution import LiveExecutionService

router = APIRouter()
repo = MarketRepository()
paper = PaperTradingEngine()
audit = AuditService()
ai_repo = AIRepository()
live_service = LiveExecutionService()


@router.get("/snapshot")
def snapshot():
    cache = repo.dashboard_snapshot()
    paper_summary = paper.summary()
    risk_state = paper_summary["risk_state"]
    portfolio = paper_summary["portfolio"]
    recent_audit = audit.recent(limit=10)
    recent_ai = ai_repo.recent(limit=10)
    live_config = live_service.get_config()
    live_wallet_status = live_service.wallet_status()
    live_requests = live_service.list_requests(limit=10)
    return {
        "pnl": paper_summary["realized_pnl"],
        "roi": paper_summary["realized_pnl"] / 10000 if paper_summary["total_trades"] else 0.0,
        "win_rate": paper_summary["win_rate"],
        "open_positions": paper_summary["open_positions"],
        "daily_target_hit": paper_summary["realized_pnl"] >= risk_state["daily_profit_target"],
        "drawdown": abs(min(0.0, paper_summary["realized_pnl"])) / 10000,
        "risk_mode": "paused" if risk_state["paused"] else "normal",
        "paper_trading": paper_summary,
        "market_cache": cache,
        "portfolio": portfolio,
        "risk_state": risk_state,
        "recent_audit": recent_audit,
        "recent_ai_decisions": recent_ai,
        "live_config": live_config,
        "live_wallet_status": live_wallet_status,
        "live_requests": live_requests,
        "alerts": [
            "paper trading ativo",
            f"{cache['active_markets']} mercados ativos em cache",
            f"{cache['books_cached']} books persistidos",
            f"{paper_summary['open_positions']} posições abertas no motor paper",
            f"risk pause={risk_state['paused']} motivo={risk_state['pause_reason'] or 'none'}",
        ],
    }
