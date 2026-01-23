from sqlalchemy import func, select

from src.repositories.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm
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
