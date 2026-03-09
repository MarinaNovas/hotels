from datetime import date

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import check_date_to_after_date_from
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            date_from,
            date_to,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
            title=title,
            location=location,
        )

    async def get_hotel(self, hotel_id):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        result = await self.db.hotels.add(data)
        await self.db.commit()
        return result

    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, data: HotelPATCH):
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
