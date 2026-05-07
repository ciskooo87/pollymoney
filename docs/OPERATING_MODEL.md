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
