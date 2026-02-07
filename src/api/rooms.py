from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import (
    RoomAdd,
    RoomAddFullRequest,
    RoomPatch,
    RoomPatchRequestFull,
)

router = APIRouter(prefix='/hotels', tags=['Комнаты'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
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
):
    result = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return result


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    result = await db.rooms.get_one_or_none_with_rls(id=room_id, hotel_id=hotel_id)
    return result


@router.post('/{hotel_id}/rooms')
async def post_room(db: DBDep, hotel_id: int, data: RoomAddFullRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    result = await db.rooms.add(room_data)

    room_facilities_data = [
        RoomFacilityAdd(room_id=result.id, facility_id=f_id) for f_id in data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {'SUCCESS': 'OK', 'result': result}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(db: DBDep, hotel_id, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.put('/{hotel_id}/rooms/{room_id}')
async def put_room(db: DBDep, hotel_id: int, room_id: int, data: RoomAddFullRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=data.facilities_ids
    )
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_room(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequestFull):
    room_data_dict = data.model_dump(exclude_unset=True)
    room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
    print(room_data)
    await db.rooms.edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if 'facilities_ids' in room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data_dict['facilities_ids']
        )
    await db.commit()
    return {'SUCCESS': 'OK'}
