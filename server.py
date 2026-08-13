import os

from fastapi.concurrency import asynccontextmanager
from fastapi import FastAPI, staticfiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn


from redis import asyncio as aioredis

import controllers
from utils.application_utils import load_routers



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connexion à Redis au démarrage de l'application
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Optionnel : déconnexion propre si nécessaire lors de la fermeture
    await redis.close()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))


async def lifespan(app: FastAPI):
    # Connexion à Redis au démarrage de l'application
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Optionnel : déconnexion propre si nécessaire lors de la fermeture
    await redis.close()

app = FastAPI(lifespan=lifespan)

app.mount('/public', staticfiles.StaticFiles(directory='api/static'))

# charger tous les router se trouvant dans controllers
load_routers(app, controllers)

if __name__ == '__main__':
    # exposer FastAPI sur le port 8000
    uvicorn.run(
        'server:app', 
        host='127.0.0.1',
        port=8000,
        reload=True
    )
