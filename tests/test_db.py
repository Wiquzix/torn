import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.wallet import WalletRequest

SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with TestingSessionLocal() as session:
        yield session

def test_create_wallet_request(session):
    wallet_data = {
        "wallet_address": "TZ4UXDJ5VXRRN5AK89WAVCGKZMZ598QBYW",
        "bandwidth": 1500,
        "energy": 2000,
        "trx_balance": 100.5
    }
    
    db_wallet = WalletRequest(**wallet_data)
    session.add(db_wallet)
    session.commit()
    session.refresh(db_wallet)
    
    saved_wallet = session.query(WalletRequest).first()
    assert saved_wallet.wallet_address == wallet_data["wallet_address"]
    assert saved_wallet.bandwidth == wallet_data["bandwidth"]
    assert saved_wallet.energy == wallet_data["energy"]
    assert saved_wallet.trx_balance == wallet_data["trx_balance"] 