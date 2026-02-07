from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAddFullRequest(RoomAddRequest):
    facilities_ids: list[int] = []


class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRls(Room):
    facilities: list[Facility] = []


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchRequestFull(RoomPatchRequest):
    facilities_ids: list[int] = []


class RoomPatch(RoomPatchRequest):
    hotel_id: int
