import asyncio

from app.services.polymarket_client import PolymarketClient
from app.workers.celery_app import celery_app


@celery_app.task
def refresh_market_data():
    client = PolymarketClient()
    data = asyncio.run(client.get_simplified_markets())
    return {"status": "ok", "task": "refresh_market_data", "count": data.get("count")}


@celery_app.task
def run_strategy_cycle():
    return {"status": "ok", "task": "run_strategy_cycle"}
