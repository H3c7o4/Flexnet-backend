from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import requests

import pandas as pd

from .. import schemas
from ..database import get_db
from ..hashing import Hash
from ..models import User, Movie
from ..oauth2 import get_current_user
from ..oauth2 import get_current_user

file = '/home/hector/Flexnet-backend/flexnet/routers/top10K-TMDB-movies.csv'
movies = pd.read_csv(file)
movies = movies[['id', 'title', 'genre', 'overview']]
movies['tags'] = movies['overview'] + movies['genre']
new_data = movies.drop(columns=['overview', 'genre'])



router = APIRouter(
    prefix='/movies',
    tags=['Movies']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_films(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db),
        get_current_user: schemas.User = Depends(get_current_user)):

    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

#@router.get('/tmdb')
#async def get_film_from_tmdb():


@router.get('/{film_id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(film_id: int,
                    db: Session = Depends(get_db),
                    get_current_user: schemas.User = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.film_id == film_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Movie with the id {film_id} is not available')
    return movie



#@router.get('/categories')
#def get_film_categories():