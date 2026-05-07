from __future__ import annotations

import asyncio
import contextlib
import json
from collections import deque
from typing import Any

import websockets

from app.core.config import settings


class PolymarketStreamManager:
    def __init__(self):
        self.market_ws = None
        self.user_ws = None
        self.market_events: deque[dict[str, Any]] = deque(maxlen=500)
        self.user_events: deque[dict[str, Any]] = deque(maxlen=500)
        self.subscribed_assets: set[str] = set()
        self.subscribed_markets: set[str] = set()
        self._market_reader_task: asyncio.Task | None = None
        self._user_reader_task: asyncio.Task | None = None
        self._market_ping_task: asyncio.Task | None = None
        self._user_ping_task: asyncio.Task | None = None

    def _channel_url(self, channel: str) -> str:
        base = settings.polymarket_ws_url.rstrip("/")
        if base.endswith("/ws"):
            return f"{base}/{channel}"
        if base.endswith("/ws-subscriptions-clob.polymarket.com"):
            return f"{base}/ws/{channel}"
        return f"{base}/{channel}"

    async def connect_market(self, asset_ids: list[str], level: int = 2, initial_dump: bool = True, custom_feature_enabled: bool = True):
        if self.market_ws is None:
            self.market_ws = await websockets.connect(self._channel_url("market"))
            self._market_reader_task = asyncio.create_task(self._reader(self.market_ws, self.market_events))
            self._market_ping_task = asyncio.create_task(self._pinger(self.market_ws))

        payload = {
            "assets_ids": asset_ids,
            "type": "market",
            "level": level,
            "initial_dump": initial_dump,
            "custom_feature_enabled": custom_feature_enabled,
        }
        await self.market_ws.send(json.dumps(payload))
        self.subscribed_assets.update(asset_ids)
        return payload

    async def update_market_subscriptions(self, operation: str, asset_ids: list[str]):
        if self.market_ws is None:
            raise RuntimeError("market websocket is not connected")
        payload = {"operation": operation, "assets_ids": asset_ids}
        await self.market_ws.send(json.dumps(payload))
        if operation == "subscribe":
            self.subscribed_assets.update(asset_ids)
        elif operation == "unsubscribe":
            self.subscribed_assets.difference_update(asset_ids)
        return payload

    async def connect_user(self, auth: dict[str, str], markets: list[str] | None = None):
        if self.user_ws is None:
            self.user_ws = await websockets.connect(self._channel_url("user"))
            self._user_reader_task = asyncio.create_task(self._reader(self.user_ws, self.user_events))
            self._user_ping_task = asyncio.create_task(self._pinger(self.user_ws))

        payload: dict[str, Any] = {"auth": auth, "type": "user"}
        if markets:
            payload["markets"] = markets
            self.subscribed_markets.update(markets)
        await self.user_ws.send(json.dumps(payload))
        return payload

    async def update_user_subscriptions(self, operation: str, markets: list[str]):
        if self.user_ws is None:
            raise RuntimeError("user websocket is not connected")
        payload = {"operation": operation, "markets": markets}
        await self.user_ws.send(json.dumps(payload))
        if operation == "subscribe":
            self.subscribed_markets.update(markets)
        elif operation == "unsubscribe":
            self.subscribed_markets.difference_update(markets)
        return payload

    async def disconnect_all(self):
        for task in [self._market_ping_task, self._market_reader_task, self._user_ping_task, self._user_reader_task]:
            if task:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
        for ws in [self.market_ws, self.user_ws]:
            if ws is not None:
                await ws.close()
        self.market_ws = None
        self.user_ws = None
        self.subscribed_assets.clear()
        self.subscribed_markets.clear()

    async def _reader(self, socket, buffer: deque[dict[str, Any]]):
        async for raw_message in socket:
            if raw_message == "PONG":
                continue
            try:
                data = json.loads(raw_message)
            except json.JSONDecodeError:
                data = {"raw": raw_message}
            buffer.append(data)

    async def _pinger(self, socket):
        while True:
            await asyncio.sleep(10)
            await socket.send("PING")

    def get_status(self) -> dict[str, Any]:
        return {
            "market_connected": self.market_ws is not None,
            "user_connected": self.user_ws is not None,
            "subscribed_assets": sorted(self.subscribed_assets),
            "subscribed_markets": sorted(self.subscribed_markets),
            "market_events_cached": len(self.market_events),
            "user_events_cached": len(self.user_events),
        }

    def recent_market_events(self, limit: int = 25) -> list[dict[str, Any]]:
        return list(self.market_events)[-limit:]

    def recent_user_events(self, limit: int = 25) -> list[dict[str, Any]]:
        return list(self.user_events)[-limit:]


stream_manager = PolymarketStreamManager()
