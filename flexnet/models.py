import pickle

from fastapi import Depends
from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, get_db

import csv
import requests

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


path_movies = '../flexnet-backend/flexnet/routers/movies_list.pkl'
p_movies = pickle.load(open(path_movies, "rb"))

list_of_all_movies = []
for i in range(10000):
    movie_dic = {}
    movie_dic['id'] = int(p_movies['id'][i])
    movie_dic['title'] = p_movies['title'][i]
    movie_dic['tags'] = p_movies['tags'][i]
    list_of_all_movies.append(movie_dic)

db = SessionLocal()

# Parcourir chaque ligne du DataFrame

for elt in list_of_all_movies:
    film_id = elt['id']
    title = elt['title']
    overview = elt['tags']


    """
    # Requête à l'API TMDB pour récupérer le lien d'image
    api_key = "f81b405a508b46f17af55c1c0876fb15"
    endpoint = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={api_key}"
    response = requests.get(url=endpoint)
    data = response.json()
    poster_path = data.get('poster_path', '')
    image = 'https://image.tmdb.org/t/p/w500' + poster_path
    """


    # Création de l'objet Film
    film = Movie(film_id=film_id, title=title, overview=overview)
    #film = Movie(film_id=film_id, title=title, overview=overview, image=image)
    #film = Movie(film_id=film_id, title=title, genre=genre, overview=overview, image=image)

    # Ajout de l'objet Film à la session de la base de données
    db.add(film)

# Validation des modifications dans la base de données
db.commit()
db.close()
