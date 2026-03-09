from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import EmailNotRegisteredException, IncorrectPasswordException, ObjectAlreadyExistsException, \
    UserAlreadyExistsException
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

class UserEmailAlreadyExistsHTTPException:
    pass

@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"SUCCESS": "OK"}

class EmailNotRegisteredHTTPException:
    pass

class IncorrectPasswordHTTPException:
    pass

@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
    )


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_one_or_none_user(user_id)
