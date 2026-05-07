from app.strategies.base import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    name = "mean_reversion"

    def generate_signals(self):
        return [{"strategy": self.name, "market": "btc-recession-impact", "confidence": 0.67, "edge": 0.017}]
