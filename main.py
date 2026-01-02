from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()
hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"},
    {"id": 3, "title": "Paris"},
    {"id": 4, "title": "Rome"},
    {"id": 5, "title": "Barcelona"},
    {"id": 6, "title": "Istanbul"},
    {"id": 7, "title": "New York"},
    {"id": 8, "title": "Tokyo"},
    {"id": 9, "title": "Bangkok"},
    {"id": 10, "title": "Bali"},
    {"id": 11, "title": "Prague"},
    {"id": 12, "title": "Vienna"},
    {"id": 13, "title": "Berlin"},
    {"id": 14, "title": "Amsterdam"},
    {"id": 15, "title": "Lisbon"},
]

@app.get("/")
def func():
    return hotels

@app.get("/hotels")
def get_hotels(id:int |None = Query(None, description="Айдишник"), title: str | None =  Query(None, description="Наименование")):
    hotels_sort = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_sort.append(hotel)
    # return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]
    return hotels_sort

@app.delete("/hotels/{hotel_id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"SUCCESS": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
