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


## Beat/Cron interno

Refresh automático configurado:
- markets simplificados: a cada 15 minutos
- order books: a cada 5 minutos

Observação: books públicos podem voltar vazios para muitos assets, então ausência de book não deve ser tratada como falha isolada.


## Paper trading engine

O motor paper roda ciclos automáticos, tenta abrir posições a partir dos sinais ranqueados, marca posições abertas a mercado e fecha trades por alvo, stop simplificado ou timeout operacional.


## Risk engine soberano

O sistema mantém um estado diário de risco com pausa automática por:
- meta diária atingida
- stop diário atingido
- max drawdown
- sequência de perdas

Além disso, expõe gross exposure e distribuição por estratégia no portfolio manager.


## IA explicável

Antes de abrir um trade paper, o engine gera uma decisão analítica persistida com:
- confidence score
- probability estimate
- risk classification
- trade rank score
- justification textual

Essas decisões ficam disponíveis por API e aparecem no dashboard/audit trail.
