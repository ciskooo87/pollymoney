from fastapi import APIRouter

from app.services.market_repository import MarketRepository
from app.services.paper_trading import PaperTradingEngine

router = APIRouter()
repo = MarketRepository()
paper = PaperTradingEngine()


@router.get("/snapshot")
def snapshot():
    cache = repo.dashboard_snapshot()
    paper_summary = paper.summary()
    risk_state = paper_summary["risk_state"]
    portfolio = paper_summary["portfolio"]
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
        "alerts": [
            "paper trading ativo",
            f"{cache['active_markets']} mercados ativos em cache",
            f"{cache['books_cached']} books persistidos",
            f"{paper_summary['open_positions']} posições abertas no motor paper",
            f"risk pause={risk_state['paused']} motivo={risk_state['pause_reason'] or 'none'}",
        ],
    }
