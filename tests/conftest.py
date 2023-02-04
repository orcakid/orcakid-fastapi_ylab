from httpx import AsyncClient
import pytest
from my_api.main import app
import pytest_asyncio

import asyncio


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest_asyncio.fixture(scope="session")
async def async_app_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
