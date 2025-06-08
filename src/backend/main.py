from fastapi import FastAPI
import requests
import random

app = FastAPI()

OMDB_API_KEY = "246ed8c1"
ANIME_MOVIES = [
    {"id": "tt0876563", "title": "Ponyo"},
    {"id": "tt5311514", "title": "Your Name"},
    {"id": "tt5323662", "title": "A Silent Voice"},
    {"id": "tt9426210", "title": "Weathering with You"},
    {"id": "tt11032374", "title": "Demon Slayer: Mugen Train"},
    {"id": "tt16183464", "title": "One Piece Film: Red"},
    {"id": "tt5914996", "title": "Nôgêmu nôraifu: Zero"},
    {"id": "tt9239552", "title": "KonoSuba: Legend of Crimson"},
    {"id": "tt27329086", "title": "Kono Subarashii Sekai ni Bakuen wo!"},
    {"id": "tt6634906", "title": "Gekijouban soushuuhen Ôbârôdo: Fushisha no ou"},
    {"id": "tt6768600", "title": "Sword Oratoria: Is It Wrong to Try to Pick Up Girls in a Dungeon? On the Side"},
    {"id": "tt1636780", "title": "Gekijôban Gintama: Shin'yaku Benizakura hen"}, 
]

MOVIES = [
    {"id": "tt3566834", "title": "Minecraft, le film"},
    {"id": "tt0060474", "title": "La Grande Vadrouille"},
    {"id": "tt0119038", "title": "Le Dîner de cons"},
    {"id": "tt1677720", "title": "Ready Player One"},
    {"id": "tt8946378", "title": "À couteaux tirés"},
]




# Récupérer tout les films
films = []
def fetch_films():
    films.clear()
    for movie in MOVIES:
        url = f"http://www.omdbapi.com/?i={movie['id']}&apikey={OMDB_API_KEY}&plot=full"
        response = requests.get(url)
        data = response.json()
        if data["Response"] == "True":
            films.append({
                "id": data["imdbID"],
                "title": data["Title"],
                "description": data["Plot"],
                "posterUrl": data["Poster"],
                "lang":"fr",
            })


# Récupérer tout les animes
animes = []
def fetch_animes():
    animes.clear()
    for anime_movie in ANIME_MOVIES:
        url = f"http://www.omdbapi.com/?i={anime_movie['id']}&apikey={OMDB_API_KEY}&plot=full"
        response = requests.get(url)
        data = response.json()
        if data["Response"] == "True":
            animes.append({
                "id": data["imdbID"],
                "title": data["Title"],
                "description": data["Plot"],
                "posterUrl": data["Poster"],
                "lang":"fr",
            })


fetch_films()
fetch_animes()

# Files de tirage
film_queue = []
anime_queue = []

def get_next_item(type_: str):
    global film_queue, anime_queue

    if type_ == "film":
        if not film_queue:
            film_queue = films.copy()
            random.shuffle(film_queue)
        return film_queue.pop(0)

    elif type_ == "anime":
        if not anime_queue:
            anime_queue = animes.copy()
            random.shuffle(anime_queue)
        return anime_queue.pop(0)

    return None

@app.get("/film")
def get_film():
    return get_next_item("film")

@app.get("/anime")
def get_anime():
    return get_next_item("anime")




#    if index < 0 or index >= len(films):
#        return {"error": "Index hors limites"}
#    
#    film = films[index]
#    return {
#        "id": film["id"],
#        "title": film["title"],
#        "description": film["description"],
#        "posterUrl": film["posterUrl"],
#        "index": index,
#        "maxIndex": len(films) - 1
#    }



    #if index < 0 or index >= len(animes):
    #    return {"error": "Index hors limites"}
    
    #anime = animes[index]
    #return {
    #    "id": anime["id"],
    #    "title": anime["title"],
    #    "description": anime["description"],
    #    "posterUrl": anime["posterUrl"],
    #    "index": index,
    #    "maxIndex": len(animes) - 1
    #}