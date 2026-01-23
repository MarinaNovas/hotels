from fastapi import APIRouter

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd

from passlib.context import CryptContext

router = APIRouter(prefix='/auth', tags=['Аутентификация и авторизация'])

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    async with async_session_maker() as session:
        user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await UsersRepository(session).add(user_data)
        await session.commit()
        return {'SUCCESS': 'OK'}
