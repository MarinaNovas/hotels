from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)

        return [
            self.schema.model_validate(item, from_attributes=True)
            for item in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs = {'literal_binds': True}))
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
