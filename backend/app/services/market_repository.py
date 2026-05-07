from __future__ import annotations

import json
from uuid import uuid4

from sqlalchemy import delete, func, select

from app.db.session import SessionLocal
from app.models.market import Market, MarketOrderBook, MarketPriceHistoryPoint, MarketToken


class MarketRepository:
    def upsert_markets(self, markets: list[dict]) -> dict:
        inserted_tokens = 0
        seen_conditions: set[str] = set()
        with SessionLocal() as session:
            for item in markets:
                condition_id = (item.get("condition_id") or "").strip()
                if not condition_id or condition_id in seen_conditions:
                    continue
                seen_conditions.add(condition_id)
                rewards = item.get("rewards") or {}
                market = session.get(Market, condition_id)
                if market is None:
                    market = Market(condition_id=condition_id)
                    session.add(market)
                market.active = item.get("active", False)
                market.closed = item.get("closed", False)
                market.archived = item.get("archived", False)
                market.accepting_orders = item.get("accepting_orders", False)
                tokens = item.get("tokens", [])
                market.token_count = len(tokens)
                market.reward_min_size = rewards.get("min_size")
                market.reward_max_spread = rewards.get("max_spread")

                session.execute(delete(MarketToken).where(MarketToken.condition_id == condition_id))
                for token in tokens:
                    token_id = (token.get("token_id") or "").strip()
                    if not token_id:
                        continue
                    existing = session.get(MarketToken, token_id)
                    if existing is None:
                        existing = MarketToken(token_id=token_id, condition_id=condition_id)
                        session.add(existing)
                    existing.condition_id = condition_id
                    existing.outcome = token.get("outcome")
                    existing.price = token.get("price")
                    existing.winner = token.get("winner")
                    inserted_tokens += 1
            session.commit()
        return {"markets": len(markets), "tokens": inserted_tokens}

    def upsert_books(self, books: list[dict]) -> int:
        count = 0
        with SessionLocal() as session:
            for item in books:
                bids = item.get("bids", [])
                asks = item.get("asks", [])
                record = session.get(MarketOrderBook, item["asset_id"])
                if record is None:
                    record = MarketOrderBook(asset_id=item["asset_id"])
                    session.add(record)
                record.condition_id = item.get("market")
                record.book_hash = item.get("hash")
                record.timestamp = item.get("timestamp")
                record.best_bid = float(bids[0]["price"]) if bids else None
                record.best_ask = float(asks[0]["price"]) if asks else None
                record.bid_depth = len(bids)
                record.ask_depth = len(asks)
                record.last_trade_price = float(item["last_trade_price"]) if item.get("last_trade_price") not in (None, "") else None
                record.tick_size = item.get("tick_size")
                record.min_order_size = item.get("min_order_size")
                record.neg_risk = item.get("neg_risk")
                record.raw_bids = json.dumps(bids)
                record.raw_asks = json.dumps(asks)
                count += 1
            session.commit()
        return count

    def replace_price_history(self, asset_id: str, interval: str | None, fidelity: int | None, history: list[dict]) -> int:
        with SessionLocal() as session:
            session.execute(delete(MarketPriceHistoryPoint).where(MarketPriceHistoryPoint.asset_id == asset_id))
            for point in history:
                session.add(MarketPriceHistoryPoint(
                    id=str(uuid4()),
                    asset_id=asset_id,
                    ts=point["t"],
                    price=point["p"],
                    interval=interval,
                    fidelity=fidelity,
                ))
            session.commit()
        return len(history)

    def dashboard_snapshot(self) -> dict:
        with SessionLocal() as session:
            total_markets = session.scalar(select(func.count()).select_from(Market)) or 0
            active_markets = session.scalar(select(func.count()).select_from(Market).where(Market.active.is_(True))) or 0
            books = session.scalar(select(func.count()).select_from(MarketOrderBook)) or 0
            histories = session.scalar(select(func.count()).select_from(MarketPriceHistoryPoint)) or 0
            top_books = session.execute(
                select(MarketOrderBook).order_by(MarketOrderBook.last_trade_price.desc().nullslast()).limit(10)
            ).scalars().all()
            return {
                "total_markets": total_markets,
                "active_markets": active_markets,
                "books_cached": books,
                "history_points": histories,
                "top_books": [
                    {
                        "asset_id": item.asset_id,
                        "condition_id": item.condition_id,
                        "best_bid": item.best_bid,
                        "best_ask": item.best_ask,
                        "last_trade_price": item.last_trade_price,
                    }
                    for item in top_books
                ],
            }

    def list_asset_ids(self, limit: int = 100, active_only: bool = True) -> list[str]:
        with SessionLocal() as session:
            stmt = select(MarketToken.token_id)
            if active_only:
                stmt = stmt.join(Market, Market.condition_id == MarketToken.condition_id).where(Market.active.is_(True))
            stmt = stmt.limit(limit)
            return list(session.execute(stmt).scalars().all())
