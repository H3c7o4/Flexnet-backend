from fastapi import FastAPI, Query
import pandas as pd
import csv
import typing
import re
import pydantic

app = FastAPI()


csv_file = 'Flexnet-backend/movies_db/top10K-TMDB-movies.csv'

#Define a route to retrieve all the list of movies in the database
@app.get('/movies/')
def movies():

    if not csv_file:    # Check for Dataset in the database
        return {"Error": "No Movie Data set"}
    
    # initialized an empty list to store the all the retrieved list of movies
    all_movies = []

    # open csv file and read its content using csv.DictReader
    with open(csv_file, mode='r', newline='') as file:

        # csv.DictReadeer reads csv files and treats each row as a dictionary
        # And treats the column headers as the keys
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
                # loops through all the list of movies in the data set
                all_movies.append(row)

    #returns all the list of movies
    return all_movies



@app.get('/list_movies_by_genre/{genre}')
def list_movies_by_genre(genre: str):
    if not csv_file:
        return {"Error": "No Movie Data set"}
    
    movies_by_genre = []

    with open(csv_file, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            #check if the genre matches the specified genre
            if row['genre'] == genre:
                movies_by_genre.append(row)

    return movies_by_genre


@app.get('/search_movies')
def search_movies(title: str = Query(..., description="Enter a Movie title to search")):
    if not csv_file:
        return {"Error": "No Movie Data set"}

    # Initialize an empty list to store matching movie recommendations
    matching_movies = []

    # Open the CSV file and read its contents using the csv.reader
    with open(csv_file, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        # Using regex to match the movie title
        for row in csv_reader:
            if re.search(re.escape(title), row['title'], re.IGNORECASE):
                matching_movies.append(row)
            else:
                return ("No Movies Found")
    
    return matching_movies

# A route to fetch a users list of liked movies
@app.get("/{user}/{user_id}/likes")
def get_liked_movies():
    pass



# A route to update a users liked movie(s) with recently liked movie(s)
@app.post('/{users}/{user_id}/add_to_liked_movies')
def add_to_liked_movies():
    pass


# A route to delete movie(s) from the movie(s) the user has already liked
@pp.delete('/users/{user}/delete_liked')
def delete_liked_movie():
    pass


# A route to delete a user from the database
@app.delete('/users/{user}/delete_user')
def delete_user():
    pass




