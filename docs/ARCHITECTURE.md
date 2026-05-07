# Arquitetura

## Visão geral

O sistema é dividido em 6 blocos principais:

1. **Ingestão de dados**
   - Polymarket REST/WebSocket
   - dados on-chain
   - notícias
   - sentimento social
   - métricas de liquidez/volume/volatilidade

2. **Camada analítica**
   - engine probabilística
   - features quantitativas
   - score de ineficiência
   - análise de sentimento
   - correlação entre mercados/eventos

3. **Camada estratégica**
   - arbitragem
   - mean reversion
   - momentum
   - sentiment trading
   - market inefficiency scanner

4. **Camada de risco**
   - sizing automático
   - limites por trade
   - stop/meta diária
   - drawdown e circuit breaker
   - redução dinâmica de exposição

5. **Camada de execução**
   - paper execution engine
   - live execution gateway
   - validação humana opcional
   - cancel/replace e encerramento de posições

6. **Camada de observabilidade**
   - dashboard
   - logs auditáveis
   - replay operacional
   - trilha de decisão da IA

## Fluxo de decisão

```text
Market Data -> Feature Engineering -> AI Scoring -> Strategy Signal
-> Risk Gate -> Execution Decision -> Order/Position Update -> Audit Log -> WebSocket Broadcast
```

## Microsserviços lógicos

Mesmo rodando inicialmente em um monorepo, o design já separa responsabilidades:

- `api-gateway`
- `market-data-service`
- `strategy-engine`
- `risk-engine`
- `execution-engine`
- `portfolio-service`
- `analytics-service`
- `notification-service`

## Segurança

- chaves privadas nunca ficam em texto puro
- live trading desabilitado por padrão
- 2FA para ações administrativas
- permissões por papel
- aprovação humana opcional para ordens

## Escalabilidade

- workers horizontais por fila
- cache Redis para snapshots
- Postgres para estado transacional
- WebSocket para streaming do dashboard
- deploy cloud-ready via containers
