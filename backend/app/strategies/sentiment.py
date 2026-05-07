from app.strategies.base import BaseStrategy

class SentimentStrategy(BaseStrategy):
    name = "sentiment"

    def generate_signals(self):
        return [{"strategy": self.name, "market": "tech-regulation-2026", "confidence": 0.69, "edge": 0.013}]
