from redis.asyncio import Redis
from app.repositories.contact_repository import ContactRepository


class RedisContactRepository(ContactRepository):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, phone: str):
        return await self.redis.get(phone)

    async def create(self, phone: str, address: str):
        await self.redis.set(phone, address)

    async def update(self, phone: str, address: str):
        await self.redis.set(phone, address)

    async def delete(self, phone: str):
        await self.redis.delete(phone)
