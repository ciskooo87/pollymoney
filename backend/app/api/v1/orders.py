from fastapi import APIRouter
from app.schemas.order import OrderRequest
from app.services.execution import ExecutionService

router = APIRouter()
service = ExecutionService()

@router.post("/simulate")
def simulate_order(payload: OrderRequest):
    return service.submit_order(payload)
