from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Наименование'),
    location: str | None = Query(None, description='Адрес'),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f'%{title.lower()}%'))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f'%{location.lower()}%'))

        query = query.limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page)

        print(query.compile(engine, compile_kwargs={'literal_binds': True}))
        result = await session.execute(query)
        # result.all() - так приходит лист из кортежей
        # result.scalar().all() - эти команды достанут из каждого кортежа превый элемент
        hotels_result = result.scalars().all()
        # print(type(hotels_result), hotels_result)
        # FastApi сам конвертируют данные к json
        return hotels_result


@router.delete('/{hotel_id}')
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]
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
        add_hotel_stmt = insert(HotelsOrm).values(**data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'SUCCESS': 'OK'}


@router.put('/{hotel_id}')
def edit_hotel(id: int, data: Hotel):
    global hotels
    hotel = next((hotel for hotel in hotels if hotel['id'] == id), None)
    if hotel:
        hotel['title'] = data.title
        hotel['name'] = data.name
        return {'SUCCESS': 'OK'}
    return {'ERROR': 'NOT FOUNT'}


@router.patch(
    '/{hotel_id}', summary='Частичное обновление отеля', description='Тут мы частично обновляем ...'
)
def patch_hotel(id: int, data: HotelPATCH):
    global hotels
    hotel = next((hotel for hotel in hotels if hotel['id'] == id), None)
    if hotel:
        if data.title:
            hotel['title'] = data.title
        if data.name:
            hotel['name'] = data.name
        return {'SUCCESS': 'OK'}
    return {'ERROR': 'NOT FOUNT'}


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
