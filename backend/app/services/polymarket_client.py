from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class PolymarketClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.polymarket_api_url).rstrip("/")

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=20.0) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()

    async def _post(self, path: str, payload: Any) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=20.0) as client:
            response = await client.post(path, json=payload)
            response.raise_for_status()
            return response.json()

    async def get_simplified_markets(self, next_cursor: str | None = None) -> dict[str, Any]:
        params = {"next_cursor": next_cursor} if next_cursor else None
        return await self._get("/simplified-markets", params=params)

    async def get_market(self, condition_id: str) -> dict[str, Any]:
        return await self._get(f"/markets/{condition_id}")

    async def get_clob_market(self, condition_id: str) -> dict[str, Any]:
        return await self._get(f"/markets/{condition_id}/clob")

    async def get_order_books(self, asset_ids: list[str]) -> list[dict[str, Any]]:
        payload = [{"token_id": asset_id} for asset_id in asset_ids]
        return await self._post("/books", payload)

    async def get_prices_history(
        self,
        market: str,
        interval: str | None = None,
        fidelity: int | None = None,
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"market": market}
        if interval:
            params["interval"] = interval
        if fidelity is not None:
            params["fidelity"] = fidelity
        if start_ts is not None:
            params["startTs"] = start_ts
        if end_ts is not None:
            params["endTs"] = end_ts
        return await self._get("/prices-history", params=params)
