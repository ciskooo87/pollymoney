from app.strategies.base import BaseStrategy

class MomentumStrategy(BaseStrategy):
    name = "momentum"

    def generate_signals(self):
        return [{"strategy": self.name, "market": "fed-rate-cut-july", "confidence": 0.74, "edge": 0.021}]
