from datetime import date

from fastapi import HTTPException
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError

from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        apartments_count = (
            select(BookingsOrm.room_id, func.count('*').label('apartments_booked'))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name='apartments_count')
        )

        apartments_left_table = (
            select(
                self.model.id,
                self.model.quantity,
                (
                    self.model.quantity - func.coalesce(apartments_count.c.apartments_booked, 0)
                ).label('apartment_left'),
            )
            .select_from(self.model)
            .outerjoin(apartments_count, self.model.id == apartments_count.c.room_id)
            .cte(name='apartments_left_table')
        )

        query = (
            select(apartments_left_table)
            .select_from(apartments_left_table)
            .filter(apartments_left_table.c.apartment_left > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))

    async def add(self, data: RoomAdd):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.schema.model_validate(model, from_attributes=True)
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
where apartment_left > 0
;
"""
"""
**1**
select room_id, count(*) as apartmens_booked  from bookings
	where date_from <= '2026-07-08' and date_to >= '2026-07-01'
	group by room_id

"""
