from fastapi import APIRouter

from app.api.v1 import dashboard, markets, orders, polymarket, risk, strategies

router = APIRouter()
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(markets.router, prefix="/markets", tags=["markets"])
router.include_router(orders.router, prefix="/orders", tags=["orders"])
router.include_router(polymarket.router, prefix="/polymarket", tags=["polymarket"])
router.include_router(risk.router, prefix="/risk", tags=["risk"])
router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
