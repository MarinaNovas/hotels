from datetime import datetime, timedelta, timezone
from http.client import HTTPException

from fastapi import APIRouter, HTTPException, Response
import jwt


from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd

from passlib.context import CryptContext

router = APIRouter(prefix='/auth', tags=['Аутентификация и авторизация'])

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    async with async_session_maker() as session:
        user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await UsersRepository(session).add(user_data)
        await session.commit()
        return {'SUCCESS': 'OK'}

@router.post('/login')
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await  UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code = 401, detail = "Пользователь с таким email не зарегестрирован")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code = 401, detail = "Пароль неверный")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
