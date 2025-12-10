from abc import ABC, abstractmethod


class ContactRepository(ABC):
    @abstractmethod
    async def get(self, phone: str) -> str | None:
        pass

    @abstractmethod
    async def create(self, phone: str, address: str) -> None:
        pass

    @abstractmethod
    async def update(self, phone: str, address: str) -> None:
        pass

    @abstractmethod
    async def delete(self, phone: str) -> None:
        pass
