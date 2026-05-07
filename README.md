# Autonomous Prediction Market Trading Engine

Engine profissional para trading quantitativo em mercados preditivos, com foco inicial em integração com Polymarket, paper trading por padrão, gestão de risco rigorosa, observabilidade e arquitetura modular para evolução futura.

## Princípios

- **Paper trading por padrão**
- **Execução real opcional e explicitamente habilitada**
- **Logs auditáveis e replay operacional**
- **Múltiplas estratégias plugáveis**
- **Gestão de risco centralizada e soberana**
- **IA explicável com racional operacional persistido**

## Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, Celery
- **Frontend:** Next.js 14, React, TypeScript, Tailwind
- **Banco:** PostgreSQL
- **Cache/Fila:** Redis
- **Tempo real:** WebSocket
- **Infra:** Docker, Docker Compose, Nginx
- **Observabilidade:** logs estruturados + trilha de auditoria

## Módulos

- `backend/`: API, engine de decisão, risco, estratégias, execução, ingestão
- `frontend/`: dashboard estilo trading desk institucional
- `infra/`: compose, nginx, bootstrap de banco
- `docs/`: arquitetura, roadmap e contrato operacional

## Capacidades previstas

- Scanner de ineficiências de mercado
- Arbitragem entre mercados correlacionados
- Mean reversion, momentum e sentiment trading
- Ranking de trades com score probabilístico
- Sizing automático, stop diário, meta diária, drawdown e circuit breaker
- Replay histórico, paper trading, backtesting e comparação de estratégias
- Whale tracking, detecção de manipulação e análise temporal

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Docs API: `http://localhost:8000/docs`

## Aviso honesto

Este projeto foi estruturado para **maximizar disciplina, auditabilidade e qualidade de decisão**, não para prometer retorno garantido. Mercados preditivos têm risco real, liquidez variável, fricções operacionais e risco regulatório/técnico.
