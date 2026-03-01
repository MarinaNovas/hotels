from datetime import date

from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDatWithRlsaMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomAdd


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
        return [RoomDatWithRlsaMapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_one_or_none_with_rls(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
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
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail="Отель с таким id не существует") from err
