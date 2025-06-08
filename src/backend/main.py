from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import requests
import random

app = FastAPI()

# --- Config SQLite ---
DATABASE_URL = "sqlite:///./data/filmometre.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# --- Modèle de données ---
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(String, index=True)
    score = Column(Float)


Base.metadata.create_all(bind=engine)

# --- Dépendance pour accéder à la DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- OMDb API ---
OMDB_API_KEY = "246ed8c1"
MOVIES = [
    {"id": "tt3566834", "title": "Minecraft, le film"},
    {"id": "tt0060474", "title": "La Grande Vadrouille"},
    {"id": "tt0119038", "title": "Le Dîner de cons"},
    {"id": "tt1677720", "title": "Ready Player One"},
    {"id": "tt8946378", "title": "À couteaux tirés"},
]
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
    {"id": "tt6634906", "title": "Overlord Movie"},
    {"id": "tt6768600", "title": "Sword Oratoria"},
    {"id": "tt1636780", "title": "Gintama Movie"},
]

# --- Chargement des films depuis l'API ---
films = []
animes = []

def fetch_movies():
    for movie in MOVIES:
        url = f"http://www.omdbapi.com/?i={movie['id']}&apikey={OMDB_API_KEY}&plot=full"
        r = requests.get(url).json()
        if r["Response"] == "True":
            films.append({
                "id": r["imdbID"],
                "title": r["Title"],
                "description": r["Plot"],
                "posterUrl": r["Poster"],
                "lang": "fr"
            })

def fetch_animes():
    for movie in ANIME_MOVIES:
        url = f"http://www.omdbapi.com/?i={movie['id']}&apikey={OMDB_API_KEY}&plot=full"
        r = requests.get(url).json()
        if r["Response"] == "True":
            animes.append({
                "id": r["imdbID"],
                "title": r["Title"],
                "description": r["Plot"],
                "posterUrl": r["Poster"],
                "lang": "fr"
            })

fetch_movies()
fetch_animes()

# --- Files de tirage aléatoire (sans doublon) ---
film_queue = []
anime_queue = []

def get_next_item(type_):
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

# --- Endpoints API ---

@app.get("/film")
def get_film():
    return get_next_item("film")

@app.get("/anime")
def get_anime():
    return get_next_item("anime")

@app.post("/note")
def add_note(film_id: str, score: float, db: Session = Depends(get_db)):
    note = Note(film_id=film_id, score=score)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@app.get("/note/{film_id}")
def get_average(film_id: str, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.film_id == film_id).all()
    if not notes:
        return {"average": None}
    avg = sum(n.score for n in notes) / len(notes)
    return {"film_id": film_id, "average": avg}
