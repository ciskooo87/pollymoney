from __future__ import annotations

import time
from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.risk import RiskState
from app.models.trade import Trade


class RiskManager:
    def current_limits(self) -> dict:
        state = self.get_state()
        return {
            "daily_profit_target_pct": 2.0,
            "daily_stop_loss_pct": 1.5,
            "max_drawdown_pct": 6.0,
            "max_risk_per_trade_pct": 0.5,
            "max_concurrent_markets": state.max_concurrent_positions,
            "daily_profit_target_abs": state.daily_profit_target,
            "daily_loss_limit_abs": state.daily_loss_limit,
            "paused": state.paused,
            "pause_reason": state.pause_reason,
            "circuit_breaker": {
                "enabled": True,
                "loss_streak_limit": 4,
                "volatility_spike_threshold": 2.5,
            },
        }

    def get_state(self) -> RiskState:
        trading_day = datetime.utcnow().strftime("%Y-%m-%d")
        now = int(time.time())
        with SessionLocal() as session:
            state = session.execute(
                select(RiskState).where(RiskState.trading_day == trading_day).limit(1)
            ).scalar_one_or_none()
            if state is None:
                state = RiskState(
                    id=str(uuid4()),
                    trading_day=trading_day,
                    paused=False,
                    pause_reason=None,
                    daily_profit_target=200.0,
                    daily_loss_limit=-150.0,
                    max_drawdown_limit=-600.0,
                    current_realized_pnl=0.0,
                    current_unrealized_pnl=0.0,
                    loss_streak=0,
                    max_concurrent_positions=12,
                    max_position_size=400.0,
                    updated_ts=now,
                )
                session.add(state)
                session.commit()
                session.refresh(state)
            return state

    def refresh_state(self) -> dict:
        trading_day = datetime.utcnow().strftime("%Y-%m-%d")
        now = int(time.time())
        with SessionLocal() as session:
            state = session.execute(
                select(RiskState).where(RiskState.trading_day == trading_day).limit(1)
            ).scalar_one_or_none()
            if state is None:
                state = RiskState(
                    id=str(uuid4()),
                    trading_day=trading_day,
                    paused=False,
                    pause_reason=None,
                    daily_profit_target=200.0,
                    daily_loss_limit=-150.0,
                    max_drawdown_limit=-600.0,
                    current_realized_pnl=0.0,
                    current_unrealized_pnl=0.0,
                    loss_streak=0,
                    max_concurrent_positions=12,
                    max_position_size=400.0,
                    updated_ts=now,
                )
                session.add(state)

            realized = session.scalar(
                select(func.coalesce(func.sum(Trade.realized_pnl), 0.0)).where(
                    Trade.paper.is_(True),
                    Trade.status == "closed",
                )
            ) or 0.0
            open_positions = session.execute(
                select(Trade).where(Trade.paper.is_(True), Trade.status == "open")
            ).scalars().all()
            unrealized = 0.0
            loss_streak = 0
            recent_closed = session.execute(
                select(Trade).where(Trade.paper.is_(True), Trade.status == "closed").order_by(Trade.closed_ts.desc().nullslast()).limit(4)
            ).scalars().all()
            for trade in recent_closed:
                if (trade.realized_pnl or 0.0) < 0:
                    loss_streak += 1
                else:
                    break

            state.current_realized_pnl = float(realized)
            state.current_unrealized_pnl = float(unrealized)
            state.loss_streak = loss_streak
            state.updated_ts = now

            pause_reason = None
            paused = False
            if state.current_realized_pnl >= state.daily_profit_target:
                paused = True
                pause_reason = "daily_target_hit"
            elif state.current_realized_pnl <= state.daily_loss_limit:
                paused = True
                pause_reason = "daily_stop_hit"
            elif state.current_realized_pnl <= state.max_drawdown_limit:
                paused = True
                pause_reason = "max_drawdown_hit"
            elif state.loss_streak >= 4:
                paused = True
                pause_reason = "loss_streak_pause"
            elif len(open_positions) >= state.max_concurrent_positions:
                pause_reason = "position_limit_near"

            state.paused = paused
            state.pause_reason = pause_reason
            session.commit()
            session.refresh(state)
            return self.serialize_state(state)

    def serialize_state(self, state: RiskState) -> dict:
        return {
            "trading_day": state.trading_day,
            "paused": state.paused,
            "pause_reason": state.pause_reason,
            "daily_profit_target": state.daily_profit_target,
            "daily_loss_limit": state.daily_loss_limit,
            "max_drawdown_limit": state.max_drawdown_limit,
            "current_realized_pnl": state.current_realized_pnl,
            "current_unrealized_pnl": state.current_unrealized_pnl,
            "loss_streak": state.loss_streak,
            "max_concurrent_positions": state.max_concurrent_positions,
            "max_position_size": state.max_position_size,
            "updated_ts": state.updated_ts,
        }

    def allow_trade(self, confidence: float, edge: float, requested_size: float | None = None) -> bool:
        state = self.refresh_state()
        if state["paused"]:
            return False
        if confidence < 0.65 or edge <= 0:
            return False
        if requested_size is not None and requested_size > state["max_position_size"]:
            return False
        return True
