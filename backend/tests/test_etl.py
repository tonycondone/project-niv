import pytest


@pytest.mark.asyncio
async def test_run_etl_success(client):
    # No body required; uses default sample file
    resp = await client.post("/api/run-etl")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("success") is True
    assert "results" in data


@pytest.mark.asyncio
async def test_get_etl_data(client):
    resp = await client.get("/api/etl-data")
    assert resp.status_code == 200
    data = resp.json()
    # Ensure expected keys for frontend
    assert "processed_data" in data
    assert "charts" in data
    assert "summary" in data
