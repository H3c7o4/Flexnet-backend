from fastapi import Depends
from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, get_db

import csv
import requests
import pandas as pd

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer)
    title = Column(String)
    genre = Column(String)
    overview = Column(String)
    image = Column(String)



class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    film_id = Column(Integer, ForeignKey('movies.id'))
    value = Column(Float)
    user = relationship(User, backref='scores')
    movie = relationship(Movie, backref='scores')

"""
db = SessionLocal()

path = '/home/hector/Flexnet-backend/flexnet/routers/top10K-TMDB-movies.csv'
# Lecture du fichier CSV avec pandas
movies = pd.read_csv(path, encoding='utf-8')
df = movies[['id', 'title', 'genre', 'overview']]

# Parcourir chaque ligne du DataFrame

for index, row in df.iterrows():
    film_id = row['id']
    title = row['title']
    genre = row['genre']
    overview = row['overview']

    # Requête à l'API TMDB pour récupérer le lien d'image
    api_key = "f81b405a508b46f17af55c1c0876fb15"
    endpoint = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={api_key}"
    response = requests.get(url=endpoint)
    data = response.json()
    poster_path = data.get('poster_path', '')
    image = 'https://image.tmdb.org/t/p/w500' + poster_path

    # Création de l'objet Film
    film = Movie(film_id=film_id, title=title, genre=genre, overview=overview, image=image)

    # Ajout de l'objet Film à la session de la base de données
    db.add(film)

# Validation des modifications dans la base de données
db.commit()
db.close()
"""