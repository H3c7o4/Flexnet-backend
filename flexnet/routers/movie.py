import pickle
import requests

path_movies = '../flexnet-backend/flexnet/routers/movies_list.pkl'
path_similarity = '../flexnet-backend/flexnet/routers/similarity.pkl'

p_movies = pickle.load(open(path_movies, "rb"))
movies_list = p_movies['title'].values

similarity = pickle.load(open(path_similarity, "rb"))

API_KEY = "f81b405a508b46f17af55c1c0876fb15"
def get_genres():

    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    genres = response.json()["genres"]
    list_of_genres = []
    for genre in genres:
        list_of_genres.append(genre["name"])
    return list_of_genres

def get_category_id(category_name):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        genres = response.json()['genres']

        for genre in genres:
            if genre['name'].lower() == category_name.lower():
                return genre['id']
    return None

def get_movies_by_category(category_name):
    category_id = get_category_id(category_name)

    if category_id is None:
        return 'This category is not available'

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={category_id}"
    response = requests.get(url)

    if response.status_code == 200:
        films = response.json()['results']
        return films
    return []

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
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

def get_movie_id(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(search_url)

    if response.status_code == 200:
        movie_id = response.json()['results'][0]['id']
        return movie_id
    return None

def get_similar_movies(movie_title):
    movie_id = get_movie_id(movie_title)

    if movie_id is None:
        return f"The movie with title {movie_title} is unavailable"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        genre_ids = response.json()['genres'][0]['id']
        similar_url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_ids}&sort_by=popularity.desc&vote_count.gte=1000&vote_average.gte=7.5"
        similar_responses = requests.get(similar_url)

        if similar_responses.status_code == 200:
            similar_movies = similar_responses.json()["results"]
            recommended_movies = []
            for i in range(5):
                recommended_movies.append(similar_movies[i])
            return recommended_movies
        return None
    return None

def get_top_movies_by_category(category_name):
    category_id = get_category_id(category_name)

    if category_id is None:
        return f'The {category_name} category is unavailable'
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&sort_by=vote_average.desc&vote_count.gte=1000&with_genres={category_id}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        films = response.json()['results']
        top_movies = films[:10]
        return top_movies
    return None

def get_movies(skip, limit):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={skip}&per_page={limit}"

    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json()['results']
        return movies
    return None

def get_movie_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        movie = response.json()
        return movie
    return None

def get_movie_by_title(movie_title):
    encoded_title = requests.utils.quote(movie_title)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={encoded_title}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json()['results']

        for movie in results:
            if movie['title'].lower() == movie_title.lower():
                return movie
        return None
