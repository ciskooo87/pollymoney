from app.strategies.arbitrage import ArbitrageStrategy
from app.strategies.mean_reversion import MeanReversionStrategy
from app.strategies.momentum import MomentumStrategy
from app.strategies.sentiment import SentimentStrategy
from app.strategies.inefficiency import InefficiencyScanner

class StrategyManager:
    def __init__(self):
        self.strategies = [
            ArbitrageStrategy(),
            MeanReversionStrategy(),
            MomentumStrategy(),
            SentimentStrategy(),
            InefficiencyScanner(),
        ]

    def rank_signals(self):
        signals = []
        for strategy in self.strategies:
            signals.extend(strategy.generate_signals())
        return sorted(signals, key=lambda item: item["confidence"], reverse=True)
