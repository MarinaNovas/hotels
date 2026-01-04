from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
	{"id": 1, "title": "Sochi", "name": "Marina"},
	{"id": 2, "title": "Dubai", "name": "Palace Downtown"},
	{"id": 3, "title": "Paris", "name": "Le Meurice"},
	{"id": 4, "title": "Rome", "name": "Hotel Eden"},
	{"id": 5, "title": "Barcelona", "name": "W Barcelona"},
	{"id": 6, "title": "Istanbul", "name": "Ciragan Palace Kempinski"},
	{"id": 7, "title": "New York", "name": "The Plaza"},
	{"id": 8, "title": "Tokyo", "name": "Park Hyatt Tokyo"},
	{"id": 9, "title": "Bangkok", "name": "Mandarin Oriental"},
	{"id": 10, "title": "Bali", "name": "Four Seasons Resort"},
	{"id": 11, "title": "Prague", "name": "Hotel Kings Court"},
	{"id": 12, "title": "Vienna", "name": "Hotel Sacher"},
]


@router.get("")
def get_hotels(
	id: int | None = Query(None, description="Айдишник"),
	title: str | None = Query(None, description="Наименование")
):
	hotels_sort = []
	for hotel in hotels:
		if id and hotel["id"] != id:
			continue
		if title and hotel["title"] != title:
			continue
		hotels_sort.append(hotel)
	return hotels_sort


@router.delete("/{hotel_id}")
def delete_hotel(id: int):
	global hotels
	hotels = [hotel for hotel in hotels if hotel["id"] != id]
	return {"SUCCESS": "OK"}


@router.post("")
def create_hotel(
	data: Hotel = Body(openapi_examples={
		"1": {"summary": "Сочи",
			  "value": {
				  "title": "Sochihotel 5",
				  "name": "sochi_u_mor"
			  }},
		"dubai": {
			"summary": "Дубай",
			"value": {
				"title": "Dubai Palace",
				"name": "palace_downtown",
			},
		},
	})
):
	hotels.append({"id": hotels[-1]["id"] + 1, "title": data.title, "name": data.name})
	return {"SUCCESS": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(id: int, data: Hotel):
	global hotels
	hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
	if hotel:
		hotel["title"] = data.title
		hotel["name"] = data.name
		return {"SUCCESS": "OK"}
	return {"ERROR": "NOT FOUNT"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля", description="Тут мы частично обновляем ...")
def patch_hotel(id: int, data: HotelPATCH):
	global hotels
	hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
	if hotel:
		if data.title:
			hotel["title"] = data.title
		if data.name:
			hotel["name"] = data.name
		return {"SUCCESS": "OK"}
	return {"ERROR": "NOT FOUNT"}


'''
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
'''
