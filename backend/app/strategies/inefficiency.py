from app.strategies.base import BaseStrategy

class InefficiencyScanner(BaseStrategy):
    name = "inefficiency_scanner"

    def generate_signals(self):
        return [{"strategy": self.name, "market": "middle-east-ceasefire", "confidence": 0.76, "edge": 0.026}]
