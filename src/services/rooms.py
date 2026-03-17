from datetime import date

from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
    check_date_to_after_date_from,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomAdd, RoomAddFullRequest, RoomPatch, RoomPatchRequestFull
from src.services.base import BaseService
from src.services.hotels import HotelService

class RoomService(BaseService):
    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_with_rls(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, data: RoomAddFullRequest):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        result = await self.db.rooms.add(room_data)

        if data.facilities_ids:
            room_facilities_data = [
                RoomFacilityAdd(room_id=result.id, facility_id=f_id) for f_id in data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(room_facilities_data)
        await self.db.commit()

    async def put_room(self, hotel_id: int, room_id: int, data: RoomAddFullRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        await self.db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=data.facilities_ids
        )
        await self.db.commit()

    async def patch_room(self, hotel_id: int, room_id: int, data: RoomPatchRequestFull):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        room_data_dict = data.model_dump(exclude_unset=True)
        room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
        print(room_data)
        await self.db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
