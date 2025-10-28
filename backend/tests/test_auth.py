import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={"username": "wrong", "password": "wrong"}
        )
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_missing_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={"username": "admin"}
        )
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_protected_endpoint_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/wines/",
            json={"name": "Test Wine", "color": "red"}
        )
    
    assert response.status_code == 401
