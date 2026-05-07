"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Props = {
  liveConfig: {
    wallet_address: string | null;
    enabled: boolean;
    armed_for_execution: boolean;
    require_human_approval: boolean;
    max_live_notional: number;
    signature_type: number;
    funder_address: string | null;
  };
  liveRequests: Array<{
    id: string;
    market_id: string;
    strategy: string;
    side: string;
    size: number;
    price: number;
    status: string;
  }>;
};

export function LiveControlPanel({ liveConfig, liveRequests }: Props) {
  const [walletAddress, setWalletAddress] = useState(liveConfig.wallet_address || "");
  const [funderAddress, setFunderAddress] = useState(liveConfig.funder_address || "");
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [apiPassphrase, setApiPassphrase] = useState("");
  const [enabled, setEnabled] = useState(liveConfig.enabled);
  const [armed, setArmed] = useState(liveConfig.armed_for_execution);
  const [requireApproval, setRequireApproval] = useState(liveConfig.require_human_approval);
  const [maxLiveNotional, setMaxLiveNotional] = useState(String(liveConfig.max_live_notional));
  const [signatureType, setSignatureType] = useState(String(liveConfig.signature_type));
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);

  async function saveConfig() {
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/orders/live/config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          wallet_address: walletAddress || null,
          clob_api_key: apiKey || null,
          clob_api_secret: apiSecret || null,
          clob_api_passphrase: apiPassphrase || null,
          enabled,
          armed_for_execution: armed,
          require_human_approval: requireApproval,
          max_live_notional: Number(maxLiveNotional),
          signature_type: Number(signatureType),
          funder_address: funderAddress || null,
        }),
      });
      if (!response.ok) throw new Error(`save failed ${response.status}`);
      setMessage("Configuração salva. Recarregue a página para refletir o estado persistido.");
      setApiKey("");
      setApiSecret("");
      setApiPassphrase("");
    } catch (error) {
      setMessage(`Erro ao salvar: ${String(error)}`);
    } finally {
      setLoading(false);
    }
  }

  async function toggleArm(nextArmed: boolean) {
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/orders/live/arm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ armed: nextArmed, changed_by: "Paulo", reason: "dashboard" }),
      });
      if (!response.ok) throw new Error(`arm failed ${response.status}`);
      setArmed(nextArmed);
      setMessage(`Kill-switch atualizado: armed=${nextArmed}`);
    } catch (error) {
      setMessage(`Erro ao alterar arm: ${String(error)}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Admin live</h2>
        <span className="label">config / arm / fila</span>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="Wallet address" value={walletAddress} onChange={(e) => setWalletAddress(e.target.value)} />
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="Funder address" value={funderAddress} onChange={(e) => setFunderAddress(e.target.value)} />
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="CLOB API key" value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="CLOB API secret" value={apiSecret} onChange={(e) => setApiSecret(e.target.value)} />
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="CLOB passphrase" value={apiPassphrase} onChange={(e) => setApiPassphrase(e.target.value)} />
        <input className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm" placeholder="Max live notional" value={maxLiveNotional} onChange={(e) => setMaxLiveNotional(e.target.value)} />
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-3 text-sm text-slate-300">
        <label className="flex items-center gap-2"><input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} /> enable live config</label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={requireApproval} onChange={(e) => setRequireApproval(e.target.checked)} /> require human approval</label>
        <label className="flex items-center gap-2">signature type <input className="w-16 rounded border border-slate-800 bg-slate-950/60 px-2 py-1" value={signatureType} onChange={(e) => setSignatureType(e.target.value)} /></label>
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <button disabled={loading} onClick={saveConfig} className="rounded-xl bg-cyan-500 px-4 py-2 text-sm font-medium text-slate-950 disabled:opacity-50">Salvar config</button>
        <button disabled={loading} onClick={() => toggleArm(true)} className="rounded-xl bg-emerald-500 px-4 py-2 text-sm font-medium text-slate-950 disabled:opacity-50">Armar live</button>
        <button disabled={loading} onClick={() => toggleArm(false)} className="rounded-xl bg-rose-500 px-4 py-2 text-sm font-medium text-white disabled:opacity-50">Desarmar live</button>
      </div>

      {message ? <div className="mt-4 text-sm text-slate-400">{message}</div> : null}

      <div className="mt-6">
        <h3 className="mb-3 text-sm font-medium text-slate-200">Fila recente</h3>
        <div className="space-y-2">
          {liveRequests.length === 0 ? (
            <div className="text-sm text-slate-400">Nenhum request live ainda.</div>
          ) : (
            liveRequests.map((item) => (
              <div key={item.id} className="rounded-xl border border-slate-800 px-3 py-2 text-sm text-slate-300">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-medium">{item.strategy}</span>
                  <span>{item.status}</span>
                </div>
                <div className="mt-1 text-slate-500 break-all">{item.market_id}</div>
                <div className="mt-1 text-slate-500">{item.side} · size {item.size} · price {item.price}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
