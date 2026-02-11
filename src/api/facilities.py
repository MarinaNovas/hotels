import json

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/')
async def get_facilities(
    db: DBDep,
):
    facilities_from_cash = await redis_manager.get("facilities")
    if not facilities_from_cash:
        print('GO TO BD')
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        await redis_manager.set("facilities", json.dumps(facilities_schemas), 10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cash)
        return facilities_dicts



@router.post('/')
async def create_facility(db: DBDep, data: FacilityAdd = Body()):
    result = await db.facilities.add(data)
    await db.commit()
    return {'SUCCESS': 'OK', 'result': result}
