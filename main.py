from dbm import sqlite3

from fastapi import FastAPI
import requests
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/sum")
def sum(x: int = 0, y: int = 10):
    return x+y

@app.get("/mul")
def mul(x: int = 0, y: int = 10):
    return x*y

@app.get("/div")
def div(x: int = 0, y: int = 10):
    return x/y

@app.get("/sub")
def pow(x: int = 0, y: int = 10):
    return x**y

@app.get("/geocode")
def geocode(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"user-Agent": "Mozilla/5.0"})
    return response.json()
# http://127.0.0.1:8000/geocode?lat=50.0680275&lon=19.9098668


@app.get('/movies')
def get_movies():
    db = sqlite3.connect("movies.db")
    cursor = db.cursor()
    movies = cursor.execute("SELECT * FROM movies").fetchall()
    output = []
    for movie in movies:
        movie = {'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]}
        output.append(movie)
    return output

    
@app.get('/movies/{movie_id}')
def get_single_movie(movie_id: int):
    db = sqlite3.connect("movies.db")
    cursor = db.cursor()
    movie = cursor.execute(f"SELECT * FROM movies WHERE id = {movie_id}").fetchone()
    if movie is None:
        return {"message": "Movie not found"}
    return {'id': movie[0], 'title': movie[1], 'year': movie[2], 'actors': movie[3]}