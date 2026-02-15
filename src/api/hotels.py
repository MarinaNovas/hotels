from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.utils.redis import facilities_key_builder

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('/all')
@cache(expire=10, key_builder=facilities_key_builder)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description='Наименование'),
    location: str | None = Query(None, description='Адрес'),
):
    print('ИДУ В БД')
    return await db.hotels.get_all(
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


@router.get('')
async def get_hotels_by_time(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(
        openapi_examples={
            'default': {
                'summary': 'Пример даты заезда',
                'value': '2026-07-01',
            }
        }
    ),
    date_to: date = Query(
        openapi_examples={
            'default': {
                'summary': 'Пример даты выезда',
                'value': '2026-07-10',
            }
        }
    ),
    title: str | None = Query(None, description='Наименование'),
    location: str | None = Query(None, description='Адрес'),
):
    return await db.hotels.get_filtered_by_time(
        date_from,
        date_to,
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
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    result = await db.hotels.get_one_or_none(id=hotel_id)
    return result


@router.delete('/{hotel_id}')
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.post('')
async def create_hotel(
    db: DBDep,
    data: HotelAdd = Body(
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
    result = await db.hotels.add(data)
    await db.commit()
    return {'SUCCESS': 'OK', 'result': result}


@router.put('/{hotel_id}')
async def edit_hotel(db: DBDep, hotel_id: int, data: HotelAdd):
    await db.hotels.edit(data, id=hotel_id)
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.patch(
    '/{hotel_id}', summary='Частичное обновление отеля', description='Тут мы частично обновляем ...'
)
async def patch_hotel(db: DBDep, hotel_id: int, data: HotelPATCH):
    await db.hotels.edit(data, exclude_unset=True, id=hotel_id)
    await db.commit()
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
