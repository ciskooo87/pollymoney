export type DashboardSnapshot = {
  pnl: number;
  roi: number;
  win_rate: number;
  open_positions: number;
  daily_target_hit: boolean;
  drawdown: number;
  risk_mode: string;
  alerts: string[];
  paper_trading: {
    total_trades: number;
    open_positions: number;
    closed_trades: number;
    wins: number;
    win_rate: number;
    realized_pnl: number;
    avg_confidence: number;
  };
  market_cache: {
    total_markets: number;
    active_markets: number;
    books_cached: number;
    history_points: number;
    top_books: Array<{
      asset_id: string;
      condition_id: string;
      best_bid: number | null;
      best_ask: number | null;
      last_trade_price: number | null;
    }>;
  };
};

export type StrategyRanking = {
  strategy: string;
  market: string;
  confidence: number;
  edge: number;
};

export type WsStatus = {
  market_connected: boolean;
  user_connected: boolean;
  subscribed_assets: string[];
  subscribed_markets: string[];
  market_events_cached: number;
  user_events_cached: number;
};
