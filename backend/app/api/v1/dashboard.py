from fastapi import APIRouter

from app.services.market_repository import MarketRepository

router = APIRouter()
repo = MarketRepository()


@router.get("/snapshot")
def snapshot():
    cache = repo.dashboard_snapshot()
    return {
        "pnl": 1245.22,
        "roi": 0.081,
        "win_rate": 0.58,
        "open_positions": 7,
        "daily_target_hit": False,
        "drawdown": 0.017,
        "risk_mode": "normal",
        "market_cache": cache,
        "alerts": [
            "paper trading ativo",
            f"{cache['active_markets']} mercados ativos em cache",
            f"{cache['books_cached']} books persistidos",
        ],
    }
