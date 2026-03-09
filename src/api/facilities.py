from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService
from src.utils.redis import facilities_key_builder

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10, key_builder=facilities_key_builder)
async def get_facilities(
    db: DBDep,
):
    print("ИДУ В БД")
    return await FacilitiesService(db).get_facilities()


@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd = Body()):
    result = await FacilitiesService(db).create_facility(data)
    return {"SUCCESS": "OK", "result": result}
