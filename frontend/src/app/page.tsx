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
  const [dashboard, rankings, wsStatus] = await Promise.all([
    fetchJson<DashboardSnapshot>("/api/dashboard/snapshot"),
    fetchJson<StrategyRanking[]>("/api/strategies/rankings"),
    fetchJson<WsStatus>("/api/polymarket/ws/status"),
  ]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.12),_transparent_30%),linear-gradient(180deg,#020617_0%,#020617_100%)] p-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex items-end justify-between gap-6">
          <div>
            <p className="label mb-3">Autonomous Prediction Market Trading Engine</p>
            <h1 className="text-4xl font-semibold tracking-tight">Trading desk quantitativo para Polymarket</h1>
            <p className="mt-3 max-w-3xl text-slate-400">Arbitragem, market making, momentum, mean reversion, sentimento e gestão de risco soberana em uma única mesa operacional.</p>
          </div>
          <div className="panel min-w-64 text-right">
            <div className="label">Modo</div>
            <div className="mt-2 text-lg font-semibold text-cyan-300">Paper Trading Default</div>
            <div className="mt-3 text-sm text-slate-400">WS market: {wsStatus.market_connected ? "conectado" : "offline"}</div>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-5">
          <MetricCard label="PnL" value={`$${fmt(dashboard.pnl)}`} />
          <MetricCard label="ROI" value={pct(dashboard.roi)} />
          <MetricCard label="Win Rate" value={pct(dashboard.win_rate)} />
          <MetricCard label="Exposição" value={`${dashboard.open_positions} pos.`} />
          <MetricCard label="Drawdown" value={pct(dashboard.drawdown)} />
        </section>

        <section className="mt-6 grid gap-4 md:grid-cols-4">
          <MetricCard label="Markets em cache" value={String(dashboard.market_cache.total_markets)} />
          <MetricCard label="Markets ativos" value={String(dashboard.market_cache.active_markets)} />
          <MetricCard label="Books persistidos" value={String(dashboard.market_cache.books_cached)} />
          <MetricCard label="Histórico salvo" value={String(dashboard.market_cache.history_points)} />
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
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
                      <div className="font-medium">{item.market}</div>
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
                <h2 className="text-xl font-semibold">Top books em cache</h2>
                <span className="label">best bid / ask</span>
              </div>
              <div className="space-y-3">
                {dashboard.market_cache.top_books.length === 0 ? (
                  <div className="text-sm text-slate-400">Nenhum order book persistido ainda.</div>
                ) : (
                  dashboard.market_cache.top_books.map((book) => (
                    <div key={book.asset_id} className="rounded-xl border border-slate-800 px-4 py-3">
                      <div className="truncate font-medium text-slate-100">{book.condition_id}</div>
                      <div className="mt-2 grid grid-cols-3 gap-3 text-sm text-slate-400">
                        <div>Bid: <span className="text-emerald-300">{book.best_bid ?? "-"}</span></div>
                        <div>Ask: <span className="text-amber-300">{book.best_ask ?? "-"}</span></div>
                        <div>Last: <span className="text-cyan-300">{book.last_trade_price ?? "-"}</span></div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="panel">
              <h2 className="text-xl font-semibold">Alertas</h2>
              <ul className="mt-4 space-y-3 text-sm text-slate-300">
                {dashboard.alerts.map((alert) => <li key={alert}>• {alert}</li>)}
              </ul>
            </div>

            <div className="panel">
              <h2 className="text-xl font-semibold">Telemetria</h2>
              <div className="mt-4 space-y-3 text-sm text-slate-300">
                <div className="flex justify-between"><span>Market WS</span><span>{wsStatus.market_connected ? "online" : "offline"}</span></div>
                <div className="flex justify-between"><span>User WS</span><span>{wsStatus.user_connected ? "offline" : "reservado"}</span></div>
                <div className="flex justify-between"><span>Assets inscritos</span><span>{wsStatus.subscribed_assets.length}</span></div>
                <div className="flex justify-between"><span>Eventos market</span><span>{wsStatus.market_events_cached}</span></div>
                <div className="flex justify-between"><span>Risk mode</span><span>{dashboard.risk_mode}</span></div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
