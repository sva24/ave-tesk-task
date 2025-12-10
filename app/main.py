import logging
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from app.api.v1.contacts.router import router as contacts_router
from app.container import AppProvider

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запущено.")
    yield
    await app.state.dishka_container.close()
    logger.info("Приложение остановлено.")


app = FastAPI(title="API для контактов", lifespan=lifespan)
container = make_async_container(AppProvider(), FastapiProvider())
setup_dishka(app=app, container=container)

app.include_router(contacts_router, prefix="/api/v1")
