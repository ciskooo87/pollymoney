from app.services.market_repository import MarketRepository
from app.strategies.arbitrage import ArbitrageStrategy
from app.strategies.mean_reversion import MeanReversionStrategy
from app.strategies.momentum import MomentumStrategy
from app.strategies.sentiment import SentimentStrategy
from app.strategies.inefficiency import InefficiencyScanner


class StrategyManager:
    def __init__(self):
        self.repo = MarketRepository()
        self.strategies = [
            ArbitrageStrategy(),
            MeanReversionStrategy(),
            MomentumStrategy(),
            SentimentStrategy(),
            InefficiencyScanner(),
        ]

    def rank_signals(self):
        market_signals = self._market_backed_signals()
        if market_signals:
            return sorted(market_signals, key=lambda item: item["confidence"], reverse=True)
        signals = []
        for strategy in self.strategies:
            signals.extend(strategy.generate_signals())
        return sorted(signals, key=lambda item: item["confidence"], reverse=True)

    def _market_backed_signals(self):
        candidates = self.repo.list_signal_candidates(limit=25)
        signals = []
        strategies = ["momentum", "mean_reversion", "inefficiency_scanner", "sentiment"]
        for idx, item in enumerate(candidates):
            price = item.get("price") if item.get("price") is not None else 0.5
            edge = abs(0.5 - price) * 0.2 + 0.01
            confidence = min(0.9, 0.62 + abs(0.5 - price) * 0.6 + ((idx % 5) * 0.03))
            signals.append({
                "strategy": strategies[idx % len(strategies)],
                "market": item["market_id"],
                "asset_id": item["asset_id"],
                "confidence": round(confidence, 4),
                "edge": round(edge, 4),
            })
        return signals
