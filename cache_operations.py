import redis
import json
import os
from fastapi.encoders import jsonable_encoder


def cache_item(item, id_item, type: str):
    redis_cli = redis.Redis(host=os.environ.get("REDIS_HOST"))
    cache_value = redis_cli.get(str(item.description)+str(id_item)+type)
    if cache_value is not None:
        return json.loads(cache_value)
    else:
        cache_value = redis_cli.set(str(item.description)+str(id_item)+type, json.dumps(jsonable_encoder(item)), ex=300)
        redis_cli.close()
        

def cache_list_item(array, type: str):
    redis_cli = redis.Redis(host=os.environ.get("REDIS_HOST"))
    cache_value = redis_cli.get(str(len(array))+type)
    if cache_value is not None:
        return json.loads(cache_value)
    else:
        cache_value = redis_cli.set(str(len(array))+type, json.dumps(jsonable_encoder(array)), ex=300)
        redis_cli.close()