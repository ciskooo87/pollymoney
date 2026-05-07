# API inicial

## Health
- `GET /health`

## Dashboard
- `GET /api/dashboard/snapshot`

## Markets
- `GET /api/markets/opportunities`

## Risk
- `GET /api/risk/limits`

## Strategies
- `GET /api/strategies/rankings`

## Orders
- `POST /api/orders/simulate`

Exemplo:
```json
{
  "market_id": "us-election-2028",
  "strategy": "arbitrage",
  "side": "buy",
  "price": 0.47,
  "size": 250,
  "expected_edge": 0.034,
  "confidence": 0.81
}
```
