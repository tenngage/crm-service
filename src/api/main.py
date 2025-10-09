from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.base_class import Base
from src.db.base import engine
import src.models
from src.api.auth import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI()

app.include_router(router)
