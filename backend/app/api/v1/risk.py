from fastapi import APIRouter
from app.services.risk_manager import RiskManager

router = APIRouter()
risk_manager = RiskManager()

@router.get("/limits")
def limits():
    return risk_manager.current_limits()
