import asyncio

from app.services.market_ingestion import MarketIngestionService
from app.services.market_repository import MarketRepository
from app.workers.celery_app import celery_app


@celery_app.task
def refresh_market_data(pages: int = 1):
    service = MarketIngestionService()
    return asyncio.run(service.ingest_simplified_markets(pages=pages))


@celery_app.task
def refresh_order_books(limit: int = 50):
    repo = MarketRepository()
    service = MarketIngestionService()
    asset_ids = repo.list_asset_ids(limit=limit)
    if not asset_ids:
        return {"books": 0, "requested_assets": 0, "reason": "no cached assets"}
    return asyncio.run(service.ingest_books_for_assets(asset_ids))


@celery_app.task
def refresh_price_history(asset_id: str, interval: str = "1d", fidelity: int = 5):
    service = MarketIngestionService()
    return asyncio.run(service.ingest_price_history(asset_id=asset_id, interval=interval, fidelity=fidelity))


@celery_app.task
def run_strategy_cycle():
    return {"status": "ok", "task": "run_strategy_cycle"}
