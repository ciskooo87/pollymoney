from fastapi import APIRouter

router = APIRouter()

@router.get("/snapshot")
def snapshot():
    return {
        "pnl": 1245.22,
        "roi": 0.081,
        "win_rate": 0.58,
        "open_positions": 7,
        "daily_target_hit": False,
        "drawdown": 0.017,
        "risk_mode": "normal",
        "alerts": [
            "paper trading ativo",
            "2 mercados com baixa liquidez",
            "1 trade aguardando confirmação de score",
        ],
    }
