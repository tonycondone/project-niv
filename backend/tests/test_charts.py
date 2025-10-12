import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("chart_type", ["line", "bar", "pie", "area", "scatter"])
async def test_get_chart_config(client, chart_type):
    # Ensure data exists
    await client.get("/api/etl-data")
    resp = await client.get(f"/api/chart/{chart_type}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_flow_chart_endpoint(client):
    resp = await client.get("/api/flow-chart")
    assert resp.status_code == 200
    data = resp.json()
    assert "nodes" in data and "edges" in data
