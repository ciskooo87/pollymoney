from __future__ import annotations

import time
from uuid import uuid4

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.market import MarketOrderBook, MarketToken
from app.models.trade import Trade
from app.services.risk_manager import RiskManager
from app.services.portfolio_manager import PortfolioManager
from app.services.audit_service import AuditService
from app.services.strategy_manager import StrategyManager


class PaperTradingEngine:
    def __init__(self):
        self.strategy_manager = StrategyManager()
        self.risk_manager = RiskManager()
        self.portfolio_manager = PortfolioManager()
        self.audit_service = AuditService()

    def run_cycle(self, max_new_trades: int = 5) -> dict:
        risk_state = self.risk_manager.refresh_state()
        signals = self.strategy_manager.rank_signals()
        opened = []
        skipped = []
        self.audit_service.log(
            event_type="paper_cycle_started",
            entity_type="engine",
            message="paper trading cycle started",
            payload={"max_new_trades": max_new_trades, "risk_state": risk_state, "signal_count": len(signals)},
        )
        for signal in signals:
            if len(opened) >= max_new_trades:
                break
            market = self._find_book(signal["market"])
            token = self._find_token(signal["market"])
            if not market and not token:
                skipped.append({"market": signal["market"], "reason": "book_and_token_not_available"})
                self.audit_service.log("paper_trade_skipped", "signal", "missing market data", payload={"signal": signal, "reason": "book_and_token_not_available"})
                continue
            estimated_size = self._position_size(signal["confidence"], signal["edge"])
            if not self.risk_manager.allow_trade(signal["confidence"], signal["edge"], requested_size=estimated_size):
                skipped.append({"market": signal["market"], "reason": "risk_rejected"})
                self.audit_service.log("paper_trade_skipped", "signal", "risk manager rejected trade", payload={"signal": signal, "reason": "risk_rejected"})
                continue
            if self._has_open_trade(signal["market"], signal["strategy"]):
                skipped.append({"market": signal["market"], "reason": "already_open"})
                self.audit_service.log("paper_trade_skipped", "signal", "trade already open", payload={"signal": signal, "reason": "already_open"})
                continue
            opened.append(self._open_trade(signal, market, token, estimated_size))

        closed = self._mark_to_market_and_close()
        stats = self.summary()
        self.audit_service.log(
            event_type="paper_cycle_finished",
            entity_type="engine",
            message="paper trading cycle finished",
            payload={"opened": opened, "closed": closed, "skipped": skipped, "summary": stats},
        )
        return {
            "opened": opened,
            "closed": closed,
            "skipped": skipped,
            "risk_state": risk_state,
            "summary": stats,
        }

    def _find_book(self, condition_id: str):
        with SessionLocal() as session:
            return session.execute(
                select(MarketOrderBook).where(MarketOrderBook.condition_id == condition_id).limit(1)
            ).scalar_one_or_none()

    def _find_token(self, condition_id: str):
        with SessionLocal() as session:
            return session.execute(
                select(MarketToken).where(MarketToken.condition_id == condition_id).limit(1)
            ).scalar_one_or_none()

    def _has_open_trade(self, market_id: str, strategy: str) -> bool:
        with SessionLocal() as session:
            existing = session.execute(
                select(Trade.id).where(
                    Trade.market_id == market_id,
                    Trade.strategy == strategy,
                    Trade.status == "open",
                    Trade.paper.is_(True),
                ).limit(1)
            ).scalar_one_or_none()
            return existing is not None

    def _open_trade(self, signal: dict, book: MarketOrderBook | None, token: MarketToken | None, size: float) -> dict:
        price = self._entry_price(book, token)
        now = int(time.time())
        trade_id = str(uuid4())
        asset_id = book.asset_id if book else (token.token_id if token else None)
        trade = Trade(
            id=trade_id,
            market_id=signal["market"],
            asset_id=asset_id,
            strategy=signal["strategy"],
            side="buy",
            size=size,
            price=price,
            expected_edge=signal["edge"],
            confidence=signal["confidence"],
            status="open",
            paper=True,
            rationale=f"signal={signal['strategy']} edge={signal['edge']:.4f} confidence={signal['confidence']:.2f}",
            opened_ts=now,
        )
        with SessionLocal() as session:
            session.add(trade)
            session.commit()
        self.audit_service.log(
            event_type="paper_trade_opened",
            entity_type="trade",
            entity_id=trade_id,
            message="paper trade opened",
            payload={"signal": signal, "asset_id": asset_id, "price": price, "size": size},
        )
        return {
            "trade_id": trade_id,
            "market_id": signal["market"],
            "asset_id": asset_id,
            "price": price,
            "size": size,
        }

    def _mark_to_market_and_close(self) -> list[dict]:
        closed = []
        now = int(time.time())
        with SessionLocal() as session:
            trades = session.execute(select(Trade).where(Trade.status == "open", Trade.paper.is_(True))).scalars().all()
            for trade in trades:
                book = session.execute(
                    select(MarketOrderBook).where(MarketOrderBook.asset_id == trade.asset_id).limit(1)
                ).scalar_one_or_none()
                mark = self._mark_price(book, trade.price)
                pnl = (mark - trade.price) * trade.size
                should_close = pnl >= abs(trade.expected_edge) * trade.size or pnl <= -(0.5 * trade.expected_edge * trade.size) or (now - (trade.opened_ts or now)) > 3600
                if should_close:
                    trade.exit_price = mark
                    trade.realized_pnl = pnl
                    trade.closed_ts = now
                    trade.status = "closed"
                    self.audit_service.log(
                        event_type="paper_trade_closed",
                        entity_type="trade",
                        entity_id=trade.id,
                        message="paper trade closed",
                        payload={"market_id": trade.market_id, "exit_price": mark, "realized_pnl": pnl},
                    )
                    closed.append({
                        "trade_id": trade.id,
                        "market_id": trade.market_id,
                        "exit_price": mark,
                        "realized_pnl": pnl,
                    })
            session.commit()
        return closed

    def _entry_price(self, book: MarketOrderBook | None, token: MarketToken | None) -> float:
        if book is not None:
            raw = book.best_ask or book.last_trade_price or book.best_bid or (token.price if token and token.price is not None else 0.5)
            return self._normalize_price(raw)
        if token is not None and token.price is not None:
            return self._normalize_price(float(token.price))
        return 0.5

    def _mark_price(self, book: MarketOrderBook | None, fallback: float) -> float:
        if book is None:
            return self._normalize_price(fallback)
        raw = book.last_trade_price or book.best_bid or book.best_ask or fallback
        return self._normalize_price(raw)

    def _normalize_price(self, value: float) -> float:
        return round(min(0.99, max(0.01, float(value))), 4)

    def _position_size(self, confidence: float, edge: float) -> float:
        base = 100.0
        multiplier = max(1.0, min(4.0, confidence * 3 + edge * 20))
        return round(base * multiplier, 2)

    def summary(self) -> dict:
        with SessionLocal() as session:
            total = session.scalar(select(func.count()).select_from(Trade).where(Trade.paper.is_(True))) or 0
            open_positions = session.scalar(select(func.count()).select_from(Trade).where(Trade.paper.is_(True), Trade.status == "open")) or 0
            closed = session.scalar(select(func.count()).select_from(Trade).where(Trade.paper.is_(True), Trade.status == "closed")) or 0
            wins = session.scalar(select(func.count()).select_from(Trade).where(Trade.paper.is_(True), Trade.status == "closed", Trade.realized_pnl > 0)) or 0
            realized = session.scalar(select(func.coalesce(func.sum(Trade.realized_pnl), 0.0)).where(Trade.paper.is_(True), Trade.status == "closed")) or 0.0
            avg_conf = session.scalar(select(func.coalesce(func.avg(Trade.confidence), 0.0)).where(Trade.paper.is_(True))) or 0.0
            portfolio = self.portfolio_manager.snapshot()
            risk_state = self.risk_manager.refresh_state()
            return {
                "total_trades": int(total),
                "open_positions": int(open_positions),
                "closed_trades": int(closed),
                "wins": int(wins),
                "win_rate": (wins / closed) if closed else 0.0,
                "realized_pnl": float(realized),
                "avg_confidence": float(avg_conf),
                "portfolio": portfolio,
                "risk_state": risk_state,
            }

    def recent_trades(self, limit: int = 20) -> list[dict]:
        with SessionLocal() as session:
            trades = session.execute(select(Trade).order_by(Trade.opened_ts.desc().nullslast()).limit(limit)).scalars().all()
            return [
                {
                    "id": t.id,
                    "market_id": t.market_id,
                    "asset_id": t.asset_id,
                    "strategy": t.strategy,
                    "side": t.side,
                    "size": t.size,
                    "price": t.price,
                    "status": t.status,
                    "confidence": t.confidence,
                    "expected_edge": t.expected_edge,
                    "realized_pnl": t.realized_pnl,
                    "rationale": t.rationale,
                }
                for t in trades
            ]
