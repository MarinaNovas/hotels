from datetime import date

from fastapi import HTTPException
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDatWithRlsaMapper, RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomAdd, RoomWithRls


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids))
        )
        result = await self.session.execute(query)

        # print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))
        return [
            RoomDatWithRlsaMapper.map_to_domain_entity(item)
            for item in result.scalars().all()
        ]

    async def get_one_or_none_with_rls(self, **filter_by):
        query = select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDatWithRlsaMapper.map_to_domain_entity(model)

    async def add(self, data: RoomAdd):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Отель с таким id не существует')


"""
/*5*/
with rooms_count as (
	select room_id, count(*) as apartmens_booked  from bookings
	where date_from <= '2026-07-08' and date_to >= '2026-07-01'
	group by room_id
),
apartment_left_table as(
	select id as room_id, quantity, apartmens_booked, quantity - coalesce(apartmens_booked, 0) as apartment_left 
	from rooms
	left join rooms_count on rooms.id = rooms_count.room_id
)
select * from apartment_left_table
where apartment_left > 0 and room_id in (select id from rooms where hotel_id=4)
;

        get_rooms_by_hotel = (
            select(self.model.id)
            .select_from(self.model)
            .filter_by(self.model.hotel_id = hotel_id)
        )
"""
