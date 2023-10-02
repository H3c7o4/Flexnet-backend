from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .utils import get_genres, get_movies_by_category, recommend, p_movies, get_similar_movies, get_top_movies_by_category, get_movies, get_movie_info, get_movie_by_title

from ..database import get_db
from ..models import Movie

router = APIRouter(
    prefix='/movies',
    tags=['Movies']
)

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

@router.get('/recommend/{film_title}', status_code=status.HTTP_200_OK)
async def recommend_movie_by_film_title(film_title: str):
    condition = p_movies['title'].str.contains(film_title, case=False).any()
    if condition == False:
        return get_similar_movies(film_title)
    recommended_movies, recommended_images = recommend(film_title)
    list_of_recommended_movies = []
    for index in range(len(recommended_movies)):
        movie = get_movie_by_title(recommended_movies[index])
        list_of_recommended_movies.append(movie)
    return list_of_recommended_movies

@router.get('/recom/{category}')
async def recommend_top_movies_by_category(category: str):
    return get_top_movies_by_category(category)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_films(
        skip: int = 1,
        limit: int = 10):
    movies = get_movies(skip, limit)
    return movies


@router.get('/genres', status_code=status.HTTP_200_OK)
async def get_genres_or_categories():
    return {'Genres': get_genres()}

@router.get('/{category_name}', status_code=status.HTTP_200_OK)
def get_movies_from_a_genre(category_name: str, skip: int = 0, limit: int = 3):
    return {f'Movies from {category_name} category': get_movies_by_category(category_name)[skip:skip+limit]}


@router.get('/films/{film_id}', status_code=status.HTTP_200_OK)
def get_movie_by_id(film_id: int):
    movie = get_movie_info(film_id)
    return movie
