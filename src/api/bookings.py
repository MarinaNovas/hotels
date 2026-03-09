from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, ObjectNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_bookings_me(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, data: Annotated[BookingAddRequest, Body(...)]):
    # получить цену номеру
    # создать схему номера BookingAdd
    # добавить бронирование конкретному пользователю
    try:
        booking = await BookingService(db).add_booking(user_id, data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "result": booking}
