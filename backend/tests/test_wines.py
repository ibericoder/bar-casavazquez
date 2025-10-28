import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_wines():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/wines/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_wines_filter_red():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/wines/?color=red")
    
    assert response.status_code == 200
    wines = response.json()
    if len(wines) > 0:
        assert all(w["color"] == "red" for w in wines)

@pytest.mark.asyncio
async def test_get_wines_available_only():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/wines/?available=true")
    
    assert response.status_code == 200
    wines = response.json()
    if len(wines) > 0:
        assert all(w["available"] == True for w in wines)

@pytest.mark.asyncio
async def test_legacy_vinos_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/wines/vinos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
