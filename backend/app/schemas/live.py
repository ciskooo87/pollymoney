from pydantic import BaseModel, Field


class LiveExecutionConfigRequest(BaseModel):
    wallet_address: str | None = None
    clob_api_key: str | None = None
    clob_api_secret: str | None = None
    clob_api_passphrase: str | None = None
    enabled: bool = False
    require_human_approval: bool = True
    max_live_notional: float = Field(default=100.0, gt=0)


class LiveOrderDecisionRequest(BaseModel):
    approved: bool
    decided_by: str
    rejection_reason: str | None = None
