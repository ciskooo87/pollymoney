# Operating Model

## Modos

### Paper trading
Modo padrão. Toda ordem é simulada, persistida e exibida no dashboard.

### Live trading
Desabilitado por padrão. Requer:
- `ENABLE_LIVE_TRADING=true`
- chaves configuradas
- validações extras
- aprovação humana opcional

## Guardrails

- stop diário
- meta diária
- drawdown máximo
- limite por operação
- limite de sequência de perdas
- circuit breaker por volatilidade
- redução automática de exposição

## Replay operacional
Toda decisão importante deve gerar:
- contexto de mercado
- score de IA
- estratégia responsável
- veredito de risco
- ação executada
