from pydantic import BaseModel, Field


class LiveExecutionConfigRequest(BaseModel):
    wallet_address: str | None = None
    clob_api_key: str | None = None
    clob_api_secret: str | None = None
    clob_api_passphrase: str | None = None
    enabled: bool = False
    armed_for_execution: bool = False
    require_human_approval: bool = True
    max_live_notional: float = Field(default=100.0, gt=0)
    signature_type: int = 1
    funder_address: str | None = None


class LiveOrderDecisionRequest(BaseModel):
    approved: bool
    decided_by: str
    rejection_reason: str | None = None


class LiveArmRequest(BaseModel):
    armed: bool
    changed_by: str
    reason: str | None = None
