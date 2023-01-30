import os

import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from my_api.db.database import db_init
from my_api.main import app


def ini():
    redis = aioredis.from_url(
        f'redis://{os.environ.get("REDIS_HOST")}:6379',
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="menu-cache")


@pytest.fixture(scope="module")
def client():
    ini()
    db_init()
    client = TestClient(app=app)
    yield client
