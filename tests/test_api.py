import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"
TEST_TRON_ADDRESS = "TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb"  # Тестовый адрес в сети Nile

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_get_wallet_info():
    with TestClient(app) as client:
        response = client.post(
            "/wallet",
            params={"wallet_address": TEST_TRON_ADDRESS}
        )
        assert response.status_code == 200
        data = response.json()
        assert "wallet_address" in data
        assert "bandwidth" in data
        assert "energy" in data
        assert "trx_balance" in data

def test_get_wallet_history():
    with TestClient(app) as client:
        # Сначала создаем запись
        client.post(
            "/wallet",
            params={"wallet_address": TEST_TRON_ADDRESS}
        )
        
        # Затем получаем историю
        response = client.get("/wallet/history")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert len(data["items"]) > 0 