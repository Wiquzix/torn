from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class WalletRequest(Base):
    __tablename__ = "wallet_requests"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    trx_balance = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 