class AIService:
    def evaluate_trade(self, market_id: str, strategy: str) -> dict:
        return {
            "market_id": market_id,
            "strategy": strategy,
            "probability_estimate": 0.61,
            "risk_classification": "medium",
            "confidence_score": 0.78,
            "justification": "Liquidez aceitável, desvio estatístico relevante e sentimento neutro-positivo.",
        }
