from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db, engine, Base
from app.models.wallet import WalletRequest
from app.schemas.wallet import WalletInfo, WalletResponse, PaginationParams
from app.services.tron import TronService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TRON Wallet Info Service")
tron_service = TronService()

@app.post("/wallet", response_model=WalletInfo)
async def get_wallet_info(
    wallet_address: str,
    db: Annotated[Session, Depends(get_db)]
):
    try:
        wallet_info = await tron_service.get_wallet_info(wallet_address)
        db_wallet = WalletRequest(**wallet_info)
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
        return db_wallet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/wallet/history", response_model=WalletResponse)
async def get_wallet_history(
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    total = db.query(WalletRequest).count()
    items = db.query(WalletRequest)\
        .order_by(WalletRequest.created_at.desc())\
        .offset(pagination.skip)\
        .limit(pagination.limit)\
        .all()
    
    return WalletResponse(total=total, items=items) 