from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

#from typing import List
import requests
import pickle
#import numpy as np

from .. import schemas
from ..database import get_db
from ..hashing import Hash
from ..models import User, Movie
from ..oauth2 import get_current_user
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/movies',
    tags=['Movies']
)

path_movies = '../Flexnet-backend/flexnet/routers/movies_list.pkl'
path_similarity = '../Flexnet-backend/flexnet/routers/similarity.pkl'

p_movies = pickle.load(open(path_movies, "rb"))
movies_list = p_movies['title'].values

similarity = pickle.load(open(path_similarity, "rb"))

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f81b405a508b46f17af55c1c0876fb15&language=en-US'
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500' + poster_path
    return full_path

def recommend(movies):
    index = p_movies[p_movies['title'] == movies].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[0:5]:
        movies_id = p_movies.iloc[i[0]].id
        recommend_movie.append(p_movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

"""
#
path_movies = '../Flexnet-backend/flexnet/routers/movies_list.pkl'
p_movies = pickle.load(open(path_movies, "rb"))

list_of_all_movies = []
for i in range(10000):
    movie_dic = {}
    movie_dic['id'] = int(p_movies['id'][i])
    movie_dic['title'] = p_movies['title'][i]
    movie_dic['tags'] = p_movies['tags'][i]
    list_of_all_movies.append(movie_dic)

def movies_pages(skip: int, limit: int) -> List:
    return list_of_all_movies[skip : skip+limit]

@router.get('/', status_code=status.HTTP_200_OK)
async def get_films_from_pickle(skip: int = 0, limit: int = 2):
    movie_list = movies_pages(skip, limit)
    return {'movies': movie_list}

@router.get('/{film_id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(film_id: int,
                    db: Session = Depends(get_db)):
    for movie in list_of_all_movies:
        if movie['id'] == film_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Movie with the id {film_id} is not available')
"""

@router.get('/recommend/{title}', status_code=status.HTTP_200_OK)
async def recommend_movie(title: str, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    recommended_movies, recommended_images = recommend(title)
    list_of_recommended_movies = []
    for index in range(len(recommended_movies)):
        movie = db.query(Movie).filter(Movie.title == recommended_movies[index]).first()
        movie.image = recommended_images[index]
        list_of_recommended_movies.append(movie)
    return list_of_recommended_movies

@router.get('/', status_code=status.HTTP_200_OK)
async def get_films(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db),
        get_current_user: schemas.User = Depends(get_current_user)):

    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies


@router.get('/{film_id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(film_id: int,
                    db: Session = Depends(get_db),
                    get_current_user: schemas.User = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.film_id == film_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Movie with the id {film_id} is not available')
    return movie
