from app.strategies.base import BaseStrategy

class ArbitrageStrategy(BaseStrategy):
    name = "arbitrage"

    def generate_signals(self):
        return [{"strategy": self.name, "market": "us-election-2028", "confidence": 0.81, "edge": 0.034}]
