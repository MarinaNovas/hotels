from fastapi import Query, APIRouter, Body

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Наименование'),
    location: str | None = Query(None, description='Адрес'),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
            title=title,
            location=location,
        )

        # query = select(HotelsOrm)
        # if title:
        #     query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        # if location:
        #     query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        #
        # query = query.limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page)
        #
        # print(query.compile(engine, compile_kwargs={'literal_binds': True}))
        # result = await session.execute(query)
        # # result.all() - так приходит лист из кортежей
        # # result.scalar().all() - эти команды достанут из каждого кортежа превый элемент
        # hotels_result = result.scalars().all()
        # # print(type(hotels_result), hotels_result)
        # # FastApi сам конвертируют данные к json


@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return result


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'SUCCESS': 'OK'}


@router.post('')
async def create_hotel(
    data: Hotel = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {'title': 'Чайка', 'location': 'г. Сочи, ул. Морская 3'},
            },
            '2': {
                'summary': 'Дубай',
                'value': {
                    'title': 'Dubai Palace',
                    'location': 'г. Дубай, ул. Шейха 2',
                },
            },
        }
    ),
):
    # тут создаем объект сессии
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(data)
        await session.commit()
    return {'SUCCESS': 'OK', 'result': result}


@router.put('/{hotel_id}')
async def edit_hotel(hotel_id: int, data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data, id=hotel_id)
        await session.commit()
    return {'SUCCESS': 'OK'}


@router.patch(
    '/{hotel_id}', summary='Частичное обновление отеля', description='Тут мы частично обновляем ...'
)
async def patch_hotel(hotel_id: int, data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {'SUCCESS': 'OK'}


"""
@router.get("/sync/{id}")
def sync(id: int):
    print(f"sync {threading.active_count()}")
    print(f"sync. Start {id}: {time.time(): .2f}")
    time.sleep(3)
    print(f"sync. End {id}: {time.time(): .2f}")


@router.get("/async/{id}")
async def async_func(id: int):
    print(f"sync {threading.active_count()}")
    print(f"async. Start {id}: {time.time(): .2f}")
    await asyncio.sleep(3)
    print(f"async. End {id}: {time.time(): .2f}")
"""
