import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt", ["csv", "json", "excel"])
async def test_export_formats(client, fmt):
    # Ensure data is available by first hitting etl-data
    await client.get("/api/etl-data")
    resp = await client.get(f"/api/data/export?format={fmt}")
    assert resp.status_code == 200
