import pytest_asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from src.db.base_class import Base
import src.models

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest_asyncio.fixture(scope="session")
async def test_db_engine():

    # Creating engine for testing db
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Creating tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def get_test_db(test_db_engine):
    test_async_session = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with test_async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_user_data():
    return {
        "email": "string@gmail.com",
        "username": "string",
        "password": "string321"
    }


@pytest_asyncio.fixture
async def register_test_user(get_test_db, test_user_data):
    from src.services.user_services import register
    from src.schemas.user_schemas import UserRegister

    result = await register(get_test_db, UserRegister(**test_user_data))
    return result
