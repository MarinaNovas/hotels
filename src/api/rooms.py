from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import (
    RoomAdd,
    RoomAddFullRequest,
    RoomPatch,
    RoomPatchRequestFull,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(
        openapi_examples={
            "default": {
                "summary": "Пример даты заезда",
                "value": "2026-07-01",
            }
        }
    ),
    date_to: date = Query(
        openapi_examples={
            "default": {
                "summary": "Пример даты выезда",
                "value": "2026-07-10",
            }
        }
    ),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def post_room(db: DBDep, hotel_id: int, data: RoomAddFullRequest = Body()):
    try:
        result = await RoomService(db).create_room(hotel_id, data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"SUCCESS": "OK", "result": result}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"SUCCESS": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(db: DBDep, hotel_id: int, room_id: int, data: RoomAddFullRequest = Body()):
    await RoomService(db).put_room(hotel_id, room_id)
    return {"SUCCESS": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequestFull):
    await RoomService(db).patch_room(hotel_id, room_id)
    return {"SUCCESS": "OK"}
