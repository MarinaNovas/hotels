from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()
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
    return hotels_sort

@app.delete("/hotels/{hotel_id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"SUCCESS": "OK"}

@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    hotels.append({"id": hotels[-1]["id"]+1, "title": title})
    return {"SUCCESS": "OK"}

@app.put("/hotels/{hotel_id}")
def put_hotel(id: int, title: str = Body(embed=True), name: str = Body(embed=True)):
    hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
    if hotel:
        hotel["title"] = title
        hotel["name"] = name
        return {"SUCCESS": "OK"}
    return {"ERROR": "NOT FOUNT"}

@app.patch("/hotels/{hotel_id}")
def patch_hotel(id: int , title: str | None = Body(None, embed=True), name: str | None = Body(None, embed=True)):
    hotel = next((hotel for hotel in hotels if hotel["id"] == id), None)
    if hotel:
        if title:
            hotel["title"] = title
        if name:
            hotel["name"] = name
        return {"SUCCESS": "OK"}
    return {"ERROR": "NOT FOUNT"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
