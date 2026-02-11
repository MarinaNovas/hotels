from fastapi import APIRouter, Body, Request, Response
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.utils.redis import facilities_key_builder

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/')
@cache(expire = 10, key_builder=facilities_key_builder)
async def get_facilities(
    db: DBDep,
):
    print('ИДУ В БД')
    return await db.facilities.get_all()



@router.post('/')
async def create_facility(db: DBDep, data: FacilityAdd = Body()):
    result = await db.facilities.add(data)
    await db.commit()
    return {'SUCCESS': 'OK', 'result': result}
