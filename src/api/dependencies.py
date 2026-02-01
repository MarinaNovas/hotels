from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description='Номер страницы (>=1)')]
    per_page: Annotated[int, Query(15, ge=1, le=25, description='Элементов на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail='Вы не аутентифицированы')
    return token


def get_current_user_id(token=Depends(get_token)) -> int | None:
    data = AuthService().decode_token(token)
    return data.get('user_id', None)


UserIdDep = Annotated[int, Depends(get_current_user_id)]


# генератор - открываект контекстный менеджер и отдает сущность
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
