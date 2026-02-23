import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_session_maker, async_session_maker_null_pull, engine_null_pull
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


async def get_db_null_pull():
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pull

@pytest.fixture(scope='function')
async def db():
    async for db_ in get_db_null_pull():
        yield db_

@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/mock_hotels.json', encoding='utf-8') as file_hotels:
        hotels = json.load(file_hotels)

    with open('tests/mock_rooms.json', encoding='utf-8') as file_rooms:
        rooms = json.load(file_rooms)

    hotels_ = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms_ = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory = async_session_maker_null_pull) as db_:
        await db_.hotels.add_bulk(hotels_)
        await db_.rooms.add_bulk(rooms_)
        await db_.commit()


@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(transport = ASGITransport(app = app), base_url = 'http://test') as ac:
        yield ac

@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_database, ac):
    await ac.post('/auth/register', json={'email': 'kot@pes.com', 'password': '1234'})
