from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"}
]


@app.get("/")
def func():
    return "Hello World!!! JHJHJHJ"


@app.get("/hotels")
def func(id: int | None = Query(None, description="Айдишник"), title: str | None = Query(None, description="Название отеля")):
    return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]
'''
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    '''
