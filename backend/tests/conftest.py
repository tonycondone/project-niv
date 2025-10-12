import pytest
import httpx
from backend.main import app, etl_processor


@pytest.fixture(autouse=True)
def reset_etl_state():
    etl_processor.raw_data = None
    etl_processor.filtered_data = None
    etl_processor.etl_metadata.clear()
    yield
    etl_processor.raw_data = None
    etl_processor.filtered_data = None
    etl_processor.etl_metadata.clear()


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
