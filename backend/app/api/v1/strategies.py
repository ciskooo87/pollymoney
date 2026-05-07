from fastapi import APIRouter
from app.services.strategy_manager import StrategyManager

router = APIRouter()
manager = StrategyManager()

@router.get("/rankings")
def rankings():
    return manager.rank_signals()
