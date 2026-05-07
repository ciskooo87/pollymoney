# Banco de dados

## Tabelas principais planejadas

- `markets`
- `market_snapshots`
- `signals`
- `trades`
- `positions`
- `risk_events`
- `strategy_runs`
- `ai_decisions`
- `news_events`
- `sentiment_observations`
- `whale_movements`
- `audit_logs`
- `backtest_runs`

## Exemplo de modelo já iniciado

Tabela `trades`:
- id
- market_id
- strategy
- side
- size
- price
- expected_edge
- confidence
- status
- paper
