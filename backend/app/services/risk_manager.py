class RiskManager:
    def current_limits(self) -> dict:
        return {
            "daily_profit_target_pct": 2.0,
            "daily_stop_loss_pct": 1.5,
            "max_drawdown_pct": 6.0,
            "max_risk_per_trade_pct": 0.5,
            "max_concurrent_markets": 12,
            "circuit_breaker": {
                "enabled": True,
                "loss_streak_limit": 4,
                "volatility_spike_threshold": 2.5,
            },
        }

    def allow_trade(self, confidence: float, edge: float) -> bool:
        return confidence >= 0.65 and edge > 0
