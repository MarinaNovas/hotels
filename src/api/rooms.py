from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=['Комнаты'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
        return result


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        return result


@router.post('/{hotel_id}/rooms')
async def post_room(hotel_id: int, data: RoomAddRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {'SUCCESS': 'OK', 'result': result}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(hotel_id, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'SUCCESS': 'OK'}


@router.put('/{hotel_id}/rooms/{room_id}')
async def put_room(hotel_id: int, room_id: int, data: RoomAddRequest = Body()):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'SUCCESS': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_room(hotel_id: int, room_id: int, data: RoomPatchRequest):
    room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        await session.commit()
    return {'SUCCESS': 'OK'}
