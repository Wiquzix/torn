from pydantic import BaseModel, Field, validator
from datetime import datetime
import re

class WalletInfo(BaseModel):
    wallet_address: str
    bandwidth: int
    energy: int
    trx_balance: float
    created_at: datetime

    @validator('wallet_address')
    def validate_tron_address(cls, v):
        if not re.match('^T[1-9A-HJ-NP-Za-km-z]{33}$', v):
            raise ValueError('Invalid TRON address format')
        return v

    class Config:
        from_attributes = True

class WalletResponse(BaseModel):
    total: int
    items: list[WalletInfo]

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100) 