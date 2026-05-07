from __future__ import annotations

from app.services.market_repository import MarketRepository
from app.services.polymarket_client import PolymarketClient


class MarketIngestionService:
    def __init__(self):
        self.client = PolymarketClient()
        self.repo = MarketRepository()

    async def ingest_simplified_markets(self, pages: int = 1) -> dict:
        next_cursor = None
        total_markets = 0
        total_tokens = 0
        for _ in range(max(1, pages)):
            payload = await self.client.get_simplified_markets(next_cursor=next_cursor)
            data = payload.get("data", [])
            result = self.repo.upsert_markets(data)
            total_markets += result["markets"]
            total_tokens += result["tokens"]
            next_cursor = payload.get("next_cursor")
            if not next_cursor:
                break
        return {"markets": total_markets, "tokens": total_tokens, "next_cursor": next_cursor}

    async def ingest_books_for_assets(self, asset_ids: list[str]) -> dict:
        books = await self.client.get_order_books(asset_ids)
        count = self.repo.upsert_books(books)
        return {"books": count, "requested_assets": len(asset_ids)}

    async def ingest_price_history(self, asset_id: str, interval: str = "1d", fidelity: int = 5) -> dict:
        payload = await self.client.get_prices_history(asset_id, interval=interval, fidelity=fidelity)
        history = payload.get("history", [])
        count = self.repo.replace_price_history(asset_id, interval, fidelity, history)
        return {"asset_id": asset_id, "history_points": count}
