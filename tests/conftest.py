import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.contacts.router import router
from app.repositories.contact_repository import ContactRepository


class FakeContactRepository(ContactRepository):
    def __init__(self):
        self.store = {}

    async def get(self, phone: str) -> str | None:
        return self.store.get(phone)

    async def create(self, phone: str, address: str) -> None:
        self.store[phone] = address

    async def update(self, phone: str, address: str) -> None:
        if phone in self.store:
            self.store[phone] = address

    async def delete(self, phone: str) -> None:
        if phone in self.store:
            del self.store[phone]


class TestProvider(Provider):
    def __init__(self):
        super().__init__()
        self.fake_repo = FakeContactRepository()

    @provide(scope=Scope.APP)
    def provide_contact_repository(self) -> ContactRepository:
        return self.fake_repo


@pytest.fixture
def test_provider():
    return TestProvider()


@pytest.fixture
def app(test_provider):
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    container = make_async_container(test_provider, FastapiProvider())
    setup_dishka(container, app)

    return app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def fake_repo(test_provider):

    return test_provider.fake_repo
