from fastapi import HTTPException

from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def add_booking(self, user_id: int, data: BookingAddRequest):
        try:
            room: Room | None = await self.db.rooms.get_one(id = data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel: Hotel | None = await self.db.hotels.get_one_or_none(id = room.hotel_id)
        price = room.price
        bookings_data = BookingAdd(user_id = user_id, price = price, **data.model_dump())
        result = await self.db.bookings.add_booking(bookings_data, hotel_id = hotel.id)
        await self.db.commit()
        return  result

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)