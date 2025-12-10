import logging
from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.repositories.contact_redis import RedisContactRepository
from app.repositories.contact_repository import ContactRepository

logger = logging.getLogger(__name__)


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_redis(self) -> AsyncGenerator[Redis, None]:
        redis = Redis(host="localhost", port=6379, decode_responses=True)
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
