import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from app.container import AppProvider
from dishka import make_async_container
from app.api.v1.contacts.router import router as contacts_router

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
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
