# API inicial

## Health
- `GET /health`

## Dashboard
- `GET /api/dashboard/snapshot`

## Markets internos
- `GET /api/markets/opportunities`

## Risco
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

## Polymarket REST
- `GET /api/polymarket/markets/simplified?next_cursor=`
- `GET /api/polymarket/markets/{condition_id}`
- `GET /api/polymarket/markets/{condition_id}/clob`
- `GET /api/polymarket/books?asset_ids=id1,id2`
- `GET /api/polymarket/prices-history/{asset_id}?interval=1d&fidelity=5`

## Polymarket WebSocket control
- `POST /api/polymarket/ws/market/connect`
- `POST /api/polymarket/ws/market/subscribe`
- `POST /api/polymarket/ws/market/unsubscribe`
- `GET /api/polymarket/ws/market/events?limit=25`
- `GET /api/polymarket/ws/status`
- `POST /api/polymarket/ws/disconnect`

Payload para conectar market stream:
```json
{
  "asset_ids": ["token-id-1", "token-id-2"],
  "level": 2,
  "initial_dump": true,
  "custom_feature_enabled": true
}
```

> O canal `user` ficou reservado para a próxima etapa, quando a camada autenticada CLOB L2 e execução real/paper autenticada forem plugadas.

## Ingestão e cache local
- `POST /api/polymarket/ingest/markets?pages=1`
- `POST /api/polymarket/ingest/books?limit=50`
- `POST /api/polymarket/ingest/history/{asset_id}?interval=1d&fidelity=5`
- `GET /api/polymarket/cache/summary`

## Paper trading
- `POST /api/orders/paper/run-cycle?max_new_trades=5`
- `GET /api/orders/paper/summary`
- `GET /api/orders/paper/trades?limit=20`

## Risk
- `GET /api/risk/state`

## Audit / Replay
- `GET /api/orders/paper/audit?limit=50&event_type=`
- `GET /api/orders/paper/replay/{trade_id}`
- `GET /api/orders/paper/ai-decisions?limit=20`

## Live execution controlado
- `POST /api/orders/live/request`
- `GET /api/orders/live/requests?limit=50`
- `POST /api/orders/live/requests/{request_id}/decision`
- `GET /api/orders/live/config`
- `POST /api/orders/live/config`
