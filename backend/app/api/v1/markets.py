from fastapi import APIRouter

router = APIRouter()

@router.get("/opportunities")
def opportunities():
    return [
        {
            "market_id": "us-election-2028",
            "strategy": "arbitrage",
            "edge": 0.034,
            "confidence": 0.81,
            "risk": "medium",
        },
        {
            "market_id": "fed-rate-cut-july",
            "strategy": "sentiment_momentum",
            "edge": 0.021,
            "confidence": 0.73,
            "risk": "medium",
        },
    ]
