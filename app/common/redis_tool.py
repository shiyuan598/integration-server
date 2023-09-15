from redis import Redis
from config.setting import REDIS_HOST, REDIS_PORT, REDIS_PWD

try:
   redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)
except Exception as e:
    print('An exception occurred in redis init: ', str(e), flush=True)

def redis_get(key):
    try:
        data = redis.get(key)
        return data
    except Exception as e:
        print('An exception occurred in redis get method', str(e), flush=True)
        return None

def redis_set(name, value, ex=60*60*12):
    try:
        return redis.set(name=name, value=value, ex=ex)
    except Exception as e:
        print('An exception occurred in redis set method', str(e), flush=True)
        return False