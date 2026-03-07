from datetime import date

from fastapi import HTTPException


class BookingException(Exception):
    detail = "Упс"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(BookingException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(BookingException):
    detail = "Нет свободных номеров"


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
