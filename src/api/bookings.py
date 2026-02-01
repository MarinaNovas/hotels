from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.post('')
async def add_booking(user_id: UserIdDep, db: DBDep, data: BookingAddRequest = Body()):
    # получить цену номеру
    # создать схему номера BookingAdd
    # добавить бронирование конкретному пользователю
    room = await db.rooms.get_one_or_none(id=data.room_id)
    price = room.price
    bookings_data = BookingAdd(user_id=user_id, price = price, **data.model_dump())
    result = await db.bookings.add(bookings_data)
    await db.commit()
    return {"status":"OK", 'result': result}
