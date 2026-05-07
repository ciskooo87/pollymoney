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
    portfolio: {
      open_positions: number;
      closed_positions: number;
      gross_exposure: number;
      realized_pnl: number;
      exposure_by_strategy: Array<{ strategy: string; exposure: number }>;
    };
    risk_state: {
      trading_day: string;
      paused: boolean;
      pause_reason: string | null;
      daily_profit_target: number;
      daily_loss_limit: number;
      max_drawdown_limit: number;
      current_realized_pnl: number;
      current_unrealized_pnl: number;
      loss_streak: number;
      max_concurrent_positions: number;
      max_position_size: number;
      updated_ts: number | null;
    };
  };
  portfolio: {
    open_positions: number;
    closed_positions: number;
    gross_exposure: number;
    realized_pnl: number;
    exposure_by_strategy: Array<{ strategy: string; exposure: number }>;
  };
  recent_ai_decisions: Array<{
    id: string;
    trade_id: string | null;
    market_id: string;
    asset_id: string | null;
    strategy: string;
    confidence_score: number;
    probability_estimate: number;
    expected_edge: number;
    risk_classification: string;
    trade_rank_score: number;
    justification: string;
    features_json: string | null;
    created_ts: number;
  }>;
  recent_audit: Array<{
    id: string;
    event_type: string;
    entity_type: string;
    entity_id: string | null;
    message: string;
    payload_json: string | null;
    created_ts: number;
  }>;
  risk_state: {
    trading_day: string;
    paused: boolean;
    pause_reason: string | null;
    daily_profit_target: number;
    daily_loss_limit: number;
    max_drawdown_limit: number;
    current_realized_pnl: number;
    current_unrealized_pnl: number;
    loss_streak: number;
    max_concurrent_positions: number;
    max_position_size: number;
    updated_ts: number | null;
  };
  live_config: {
    wallet_address: string | null;
    clob_api_key: string | null;
    clob_api_secret: string | null;
    clob_api_passphrase: string | null;
    enabled: boolean;
    armed_for_execution: boolean;
    require_human_approval: boolean;
    max_live_notional: number;
    signature_type: number;
    funder_address: string | null;
    updated_ts: number | null;
  };
  live_wallet_status: {
    wallet_address: string | null;
    funder_address: string | null;
    signature_type: number;
    has_api_key: boolean;
    has_api_secret: boolean;
    has_api_passphrase: boolean;
    has_encrypted_private_key: boolean;
    has_rpc_url: boolean;
    armed_for_execution: boolean;
    runtime_live_enabled: boolean;
  };
  live_requests: Array<{
    id: string;
    market_id: string;
    asset_id: string | null;
    strategy: string;
    side: string;
    size: number;
    price: number;
    status: string;
    rationale: string | null;
    approval_required: boolean;
    approved_by: string | null;
    rejection_reason: string | null;
    created_ts: number;
    decided_ts: number | null;
  }>;
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
