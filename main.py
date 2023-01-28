from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from database import db_init
from models import Dish, Menu, Submenu
from router import router
import os

app = FastAPI()


@app.on_event('startup')
def on_startup():
    redis = aioredis.from_url(
        f'redis://{os.environ.get("REDIS_HOST")}:6379',
        encoding='utf8',
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix='menu-cache')
    db_init()


app.include_router(router=router)
