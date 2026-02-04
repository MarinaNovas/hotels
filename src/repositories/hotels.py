from datetime import date

from sqlalchemy import func, select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
        self,
        limit: int,
        offset: int,
        title: str | None,
        location: str | None,
    ) -> list[Hotel]:
        query = select(self.model)
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))

        query = query.limit(limit).offset(offset)
        print(query.compile(engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)

        return [
            self.schema.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]

    async def get_filtered_by_time(self, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from = date_from, date_to= date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(self.model.id.in_(hotels_ids_to_get))