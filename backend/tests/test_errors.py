import pytest


@pytest.mark.asyncio
async def test_get_chart_config_without_data_returns_error(client):
    # Reset state ensures no data is loaded; chart type unsupported leads to 500
    resp = await client.get("/api/chart/unknown")
    assert resp.status_code in (400, 500)


@pytest.mark.asyncio
async def test_export_unsupported_format(client):
    # Ensure some data exists first
    await client.get("/api/etl-data")
    resp = await client.get("/api/data/export?format=xml")
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_upload_invalid_file(client):
    # Use broken bytes to force pandas error during read
    content = b"\xff\xfe\x00\x00"
    files = {"file": ("bad.csv", content, "text/csv")}
    resp = await client.post("/api/upload-csv", files=files)
    assert resp.status_code in (400, 500)


@pytest.mark.asyncio
async def test_apply_filters_without_data_autoloads_or_errors(client):
    resp = await client.post("/api/apply-filters?percentage=0.1")
    assert resp.status_code in (200, 400)
