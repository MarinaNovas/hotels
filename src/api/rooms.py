from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=['Комнаты'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(db: DBDep, hotel_id: int):
    result = await db.rooms.get_filtered(hotel_id=hotel_id)
    return result


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    result = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return result


@router.post('/{hotel_id}/rooms')
async def post_room(db: DBDep, hotel_id: int, data: RoomAddRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    result = await db.rooms.add(room_data)
    await db.commit()
    return {'SUCCESS': 'OK', 'result': result}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(db: DBDep, hotel_id, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.put('/{hotel_id}/rooms/{room_id}')
async def put_room(db: DBDep, hotel_id: int, room_id: int, data: RoomAddRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'SUCCESS': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_room(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequest):
    room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    await db.commit()
    return {'SUCCESS': 'OK'}
