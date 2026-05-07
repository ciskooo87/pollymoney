export const dashboard = {
  pnl: "+$1,245.22",
  roi: "8.1%",
  winRate: "58%",
  exposure: "34%",
  drawdown: "1.7%",
  alerts: [
    "Paper trading ativo por padrão",
    "Baixa liquidez detectada em 2 mercados",
    "Circuit breaker armado: pronto para reduzir risco"
  ],
  strategies: [
    { name: "Arbitragem", sharpe: "1.82", pnl: "+$420" },
    { name: "Momentum", sharpe: "1.34", pnl: "+$310" },
    { name: "Mean Reversion", sharpe: "1.12", pnl: "+$205" },
    { name: "Sentiment", sharpe: "0.97", pnl: "+$148" }
  ],
  opportunities: [
    { market: "US Election 2028", edge: "3.4%", confidence: "0.81" },
    { market: "Fed Rate Cut July", edge: "2.1%", confidence: "0.74" },
    { market: "Ceasefire Event", edge: "2.6%", confidence: "0.76" }
  ]
};
