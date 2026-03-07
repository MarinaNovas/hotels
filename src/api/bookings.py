from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    result = await db.bookings.get_all()
    return result


@router.get("/me")
async def get_bookings_me(user_id: UserIdDep, db: DBDep):
    result = await db.bookings.get_filtered(user_id=user_id)
    return result


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, data: Annotated[BookingAddRequest, Body(...)]):
    # получить цену номеру
    # создать схему номера BookingAdd
    # добавить бронирование конкретному пользователю
    try:
        room: Room | None = await db.rooms.get_one(id=data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel: Hotel | None = await db.hotels.get_one_or_none(id=room.hotel_id)
    price = room.price
    bookings_data = BookingAdd(user_id=user_id, price=price, **data.model_dump())
    try:
        result = await db.bookings.add_booking(bookings_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "result": result}
