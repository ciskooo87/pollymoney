import { MetricCard } from "../components/MetricCard";
import { fetchJson } from "../lib/api";
import type { DashboardSnapshot, StrategyRanking, WsStatus } from "../lib/types";

function pct(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

function fmt(value: number) {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);
}

export default async function HomePage() {
  const [dashboard, rankings, wsStatus, trades] = await Promise.all([
    fetchJson<DashboardSnapshot>("/api/dashboard/snapshot"),
    fetchJson<StrategyRanking[]>("/api/strategies/rankings"),
    fetchJson<WsStatus>("/api/polymarket/ws/status"),
    fetchJson<any[]>("/api/orders/paper/trades?limit=10"),
  ]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.12),_transparent_30%),linear-gradient(180deg,#020617_0%,#020617_100%)] p-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex items-end justify-between gap-6">
          <div>
            <p className="label mb-3">Autonomous Prediction Market Trading Engine</p>
            <h1 className="text-4xl font-semibold tracking-tight">Trading desk quantitativo para Polymarket</h1>
            <p className="mt-3 max-w-3xl text-slate-400">Agora com portfolio manager, risk engine diário e circuito de pausa automática sobre o motor paper.</p>
          </div>
          <div className="panel min-w-72 text-right">
            <div className="label">Modo</div>
            <div className="mt-2 text-lg font-semibold text-cyan-300">Paper Trading Sovereign Risk</div>
            <div className="mt-3 text-sm text-slate-400">WS market: {wsStatus.market_connected ? "conectado" : "offline"}</div>
            <div className="text-sm text-slate-400">risk: {dashboard.risk_mode}</div>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-5">
          <MetricCard label="PnL" value={`$${fmt(dashboard.pnl)}`} />
          <MetricCard label="ROI" value={pct(dashboard.roi)} />
          <MetricCard label="Win Rate" value={pct(dashboard.win_rate)} />
          <MetricCard label="Posições abertas" value={String(dashboard.open_positions)} />
          <MetricCard label="Drawdown" value={pct(dashboard.drawdown)} />
        </section>

        <section className="mt-6 grid gap-4 md:grid-cols-4">
          <MetricCard label="Trades paper" value={String(dashboard.paper_trading.total_trades)} />
          <MetricCard label="Trades fechados" value={String(dashboard.paper_trading.closed_trades)} />
          <MetricCard label="Loss streak" value={String(dashboard.risk_state.loss_streak)} />
          <MetricCard label="Conf. média" value={dashboard.paper_trading.avg_confidence.toFixed(2)} />
        </section>

        <section className="mt-6 grid gap-4 md:grid-cols-4">
          <MetricCard label="Exposição bruta" value={`$${fmt(dashboard.portfolio.gross_exposure)}`} />
          <MetricCard label="Target diário" value={`$${fmt(dashboard.risk_state.daily_profit_target)}`} />
          <MetricCard label="Stop diário" value={`$${fmt(Math.abs(dashboard.risk_state.daily_loss_limit))}`} />
          <MetricCard label="Limite por posição" value={`$${fmt(dashboard.risk_state.max_position_size)}`} />
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="space-y-6">
            <div className="panel">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Ranking de sinais</h2>
                <span className="label">edge / confiança</span>
              </div>
              <div className="space-y-3">
                {rankings.map((item) => (
                  <div key={`${item.strategy}-${item.market}`} className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
                    <div>
                      <div className="font-medium break-all">{item.market}</div>
                      <div className="text-sm text-slate-400">{item.strategy}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-emerald-300">{pct(item.edge)}</div>
                      <div className="text-sm text-slate-400">conf. {item.confidence.toFixed(2)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Últimos trades paper</h2>
                <span className="label">simulados</span>
              </div>
              <div className="space-y-3">
                {trades.length === 0 ? (
                  <div className="text-sm text-slate-400">Nenhum trade paper gerado ainda.</div>
                ) : (
                  trades.map((trade) => (
                    <div key={trade.id} className="rounded-xl border border-slate-800 px-4 py-3">
                      <div className="flex items-center justify-between gap-4">
                        <div className="font-medium break-all">{trade.market_id}</div>
                        <div className={trade.status === "closed" ? "text-sm text-slate-300" : "text-sm text-cyan-300"}>{trade.status}</div>
                      </div>
                      <div className="mt-2 grid grid-cols-2 gap-2 text-sm text-slate-400">
                        <div>{trade.strategy}</div>
                        <div className="text-right">size {trade.size}</div>
                        <div>price {trade.price}</div>
                        <div className="text-right">pnl {trade.realized_pnl ?? "-"}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="panel">
              <h2 className="text-xl font-semibold">Risk engine</h2>
              <div className="mt-4 space-y-3 text-sm text-slate-300">
                <div className="flex justify-between"><span>Pausado</span><span>{dashboard.risk_state.paused ? "sim" : "não"}</span></div>
                <div className="flex justify-between"><span>Motivo</span><span>{dashboard.risk_state.pause_reason ?? "none"}</span></div>
                <div className="flex justify-between"><span>Realized PnL</span><span>{fmt(dashboard.risk_state.current_realized_pnl)}</span></div>
                <div className="flex justify-between"><span>Loss streak</span><span>{dashboard.risk_state.loss_streak}</span></div>
                <div className="flex justify-between"><span>Max posições</span><span>{dashboard.risk_state.max_concurrent_positions}</span></div>
              </div>
            </div>

            <div className="panel">
              <h2 className="text-xl font-semibold">Exposição por estratégia</h2>
              <div className="mt-4 space-y-3 text-sm text-slate-300">
                {dashboard.portfolio.exposure_by_strategy.length === 0 ? (
                  <div className="text-slate-400">Sem exposição aberta.</div>
                ) : (
                  dashboard.portfolio.exposure_by_strategy.map((item) => (
                    <div key={item.strategy} className="flex justify-between">
                      <span>{item.strategy}</span>
                      <span>${fmt(item.exposure)}</span>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className="panel">
              <h2 className="text-xl font-semibold">Alertas</h2>
              <ul className="mt-4 space-y-3 text-sm text-slate-300">
                {dashboard.alerts.map((alert) => <li key={alert}>• {alert}</li>)}
              </ul>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
