class AIService:
    def evaluate_trade(self, market_id: str, strategy: str, price: float, confidence: float, edge: float, asset_id: str | None = None) -> dict:
        distance_from_mid = abs(0.5 - price)
        probability_estimate = min(0.95, max(0.05, price + edge * 0.5))
        confidence_score = min(0.99, max(0.5, confidence * 0.85 + edge * 1.4))
        trade_rank_score = round(confidence_score * (1 + edge * 10), 4)

        if confidence_score >= 0.82 and edge >= 0.03:
            risk_classification = "low"
        elif confidence_score >= 0.7 and edge >= 0.015:
            risk_classification = "medium"
        else:
            risk_classification = "high"

        justification = (
            f"Estratégia {strategy} com preço normalizado em {price:.4f}, edge estimado de {edge:.4f}, "
            f"confiança base de {confidence:.2f} e distância do midpoint de {distance_from_mid:.4f}. "
            f"Probabilidade ajustada em {probability_estimate:.4f}; risco classificado como {risk_classification}."
        )

        return {
            "market_id": market_id,
            "asset_id": asset_id,
            "strategy": strategy,
            "probability_estimate": round(probability_estimate, 4),
            "risk_classification": risk_classification,
            "confidence_score": round(confidence_score, 4),
            "trade_rank_score": trade_rank_score,
            "expected_edge": round(edge, 4),
            "justification": justification,
            "features": {
                "price": round(price, 4),
                "distance_from_mid": round(distance_from_mid, 4),
                "base_confidence": round(confidence, 4),
                "expected_edge": round(edge, 4),
            },
        }
