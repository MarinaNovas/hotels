from sqlalchemy import select, func, insert

from repositories.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        limit: int,
        offset: int,
        title: str | None,
        location: str | None,
    ):
        query = select(self.model)
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))

        query = query.limit(limit).offset(offset)
        print(query.compile(engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)

        return result.scalars().all()
