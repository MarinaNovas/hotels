from datetime import date

from fastapi import HTTPException


class BookingException(Exception):
    detail = "Упс"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(BookingException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(BookingException):
    detail = "Нет свободных номеров"

class IncorrectTokenException(BookingException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(BookingException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BookingException):
    detail = "Пароль неверный"


class UserAlreadyExistsException(BookingException):
    detail = "Пользователь уже существуе"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда ")


class BookingNotFoundException(HTTPException):
    statu_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.statu_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingNotFoundException):
    statu_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingNotFoundException):
    statu_code = 404
    detail = "Номер не найден"

class AllRoomsAreBookedHTTPException(BookingException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(BookingException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(BookingException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(BookingException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectPasswordHTTPException(BookingException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(BookingException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"
