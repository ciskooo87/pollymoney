import { MetricCard } from "../components/MetricCard";
import { dashboard } from "../lib/mock";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.12),_transparent_30%),linear-gradient(180deg,#020617_0%,#020617_100%)] p-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex items-end justify-between">
          <div>
            <p className="label mb-3">Autonomous Prediction Market Trading Engine</p>
            <h1 className="text-4xl font-semibold tracking-tight">Trading desk quantitativo para Polymarket</h1>
            <p className="mt-3 max-w-3xl text-slate-400">Arbitragem, market making, momentum, mean reversion, sentimento e gestão de risco soberana em uma única mesa operacional.</p>
          </div>
          <div className="panel text-right">
            <div className="label">Modo</div>
            <div className="mt-2 text-lg font-semibold text-cyan-300">Paper Trading Default</div>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-5">
          <MetricCard label="PnL" value={dashboard.pnl} />
          <MetricCard label="ROI" value={dashboard.roi} />
          <MetricCard label="Win Rate" value={dashboard.winRate} />
          <MetricCard label="Exposição" value={dashboard.exposure} />
          <MetricCard label="Drawdown" value={dashboard.drawdown} />
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
          <div className="panel">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Oportunidades ranqueadas</h2>
              <span className="label">Edge / confiança</span>
            </div>
            <div className="space-y-3">
              {dashboard.opportunities.map((item) => (
                <div key={item.market} className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
                  <div>
                    <div className="font-medium">{item.market}</div>
                    <div className="text-sm text-slate-400">Scanner de ineficiência + filtro de risco</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-emerald-300">{item.edge}</div>
                    <div className="text-sm text-slate-400">conf. {item.confidence}</div>
                  </div>
                </div>
              ))}
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
              <h2 className="text-xl font-semibold">Estratégias</h2>
              <div className="mt-4 space-y-3">
                {dashboard.strategies.map((strategy) => (
                  <div key={strategy.name} className="flex justify-between rounded-xl border border-slate-800 px-4 py-3">
                    <div>
                      <div className="font-medium">{strategy.name}</div>
                      <div className="text-xs text-slate-400">Sharpe {strategy.sharpe}</div>
                    </div>
                    <div className="font-semibold text-cyan-300">{strategy.pnl}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
