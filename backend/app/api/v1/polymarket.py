from fastapi import APIRouter, HTTPException, Query

from app.schemas.polymarket import MarketSubscriptionRequest, UserSubscriptionRequest
from app.services.market_ingestion import MarketIngestionService
from app.services.market_repository import MarketRepository
from app.services.polymarket_client import PolymarketClient
from app.services.polymarket_stream import stream_manager

router = APIRouter()
client = PolymarketClient()
ingestion = MarketIngestionService()
repo = MarketRepository()


@router.get("/markets/simplified")
async def simplified_markets(next_cursor: str | None = None):
    return await client.get_simplified_markets(next_cursor=next_cursor)


@router.post("/ingest/markets")
async def ingest_markets(pages: int = 1):
    return await ingestion.ingest_simplified_markets(pages=pages)


@router.post("/ingest/books")
async def ingest_books(limit: int = 50):
    asset_ids = repo.list_asset_ids(limit=limit)
    if not asset_ids:
        raise HTTPException(status_code=400, detail="Nenhum asset_id disponível no banco. Faça ingest de markets primeiro.")
    return await ingestion.ingest_books_for_assets(asset_ids)


@router.post("/ingest/history/{asset_id}")
async def ingest_history(asset_id: str, interval: str = "1d", fidelity: int = 5):
    return await ingestion.ingest_price_history(asset_id=asset_id, interval=interval, fidelity=fidelity)


@router.get("/cache/summary")
def cache_summary():
    return repo.dashboard_snapshot()


@router.get("/markets/{condition_id}")
async def market_by_id(condition_id: str):
    return await client.get_market(condition_id)


@router.get("/markets/{condition_id}/clob")
async def clob_market_info(condition_id: str):
    return await client.get_clob_market(condition_id)


@router.get("/books")
async def books(asset_ids: str = Query(..., description="Comma-separated token ids")):
    ids = [item.strip() for item in asset_ids.split(",") if item.strip()]
    if not ids:
        raise HTTPException(status_code=400, detail="asset_ids is required")
    return await client.get_order_books(ids)


@router.get("/prices-history/{asset_id}")
async def prices_history(asset_id: str, interval: str | None = None, fidelity: int | None = None, start_ts: int | None = None, end_ts: int | None = None):
    return await client.get_prices_history(asset_id, interval=interval, fidelity=fidelity, start_ts=start_ts, end_ts=end_ts)


@router.post("/ws/market/connect")
async def connect_market_stream(payload: MarketSubscriptionRequest):
    return await stream_manager.connect_market(
        asset_ids=payload.asset_ids,
        level=payload.level,
        initial_dump=payload.initial_dump,
        custom_feature_enabled=payload.custom_feature_enabled,
    )


@router.post("/ws/market/subscribe")
async def subscribe_market_stream(payload: MarketSubscriptionRequest):
    return await stream_manager.update_market_subscriptions("subscribe", payload.asset_ids)


@router.post("/ws/market/unsubscribe")
async def unsubscribe_market_stream(payload: MarketSubscriptionRequest):
    return await stream_manager.update_market_subscriptions("unsubscribe", payload.asset_ids)


@router.get("/ws/market/events")
def market_events(limit: int = 25):
    return stream_manager.recent_market_events(limit)


@router.post("/ws/user/connect")
async def connect_user_stream(payload: UserSubscriptionRequest):
    raise HTTPException(
        status_code=501,
        detail="User WebSocket requer credenciais CLOB L2 e será habilitado junto da camada autenticada de trading.",
    )


@router.get("/ws/status")
def websocket_status():
    return stream_manager.get_status()


@router.post("/ws/disconnect")
async def disconnect_streams():
    await stream_manager.disconnect_all()
    return {"status": "disconnected"}
