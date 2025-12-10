import logging
import os
from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.repositories.contact_redis import RedisContactRepository
from app.repositories.contact_repository import ContactRepository

logger = logging.getLogger(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_redis(self) -> AsyncGenerator[Redis, None]:
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        try:
            await redis.ping()
            logger.info("Успешное подключение к Redis")
        except Exception as e:
            logger.error("Ошибка подключения к Redis: %s", e)

        yield redis
        await redis.close()

    @provide(scope=Scope.APP)
    def provide_contact_repository(self, redis: Redis) -> ContactRepository:
        return RedisContactRepository(redis)
