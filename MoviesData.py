#Importing libraries
import pandas as pd

class MoviesData:
    
    def __init__(self, conn):
        self.conn = conn
        
    #Importing data from the oracle database
    def importUsersData(self):
        conn = self.conn
        user_ratings = pd.read_sql("Select FAN_ID, FILM_ID, IMDB_RATING from RELMDB.FAN_RATINGS", conn)
        #user_ratings.head()
        return user_ratings
    
    def importMoviesData(self):
        conn = self.conn
        movies = pd.read_sql("Select FILM_ID, FILM_TITLE, FILM_YEAR, IMDB_VOTES from RELMDB.MOVIES", conn)
        #movies.head()
        return movies
    
    def importGenresData(self):
        conn = self.conn
        genres = pd.read_sql("Select FILM_ID, GENRE from RELMDB.GENRES", conn)
        #genres.head()
        return genres
    
    def importDirectorsData(self):
        conn = self.conn
        directors = pd.read_sql("Select FILM_ID, DIRECTOR FROM RELMDB.DIRECTORS", conn)
        #directors.head()
        return directors
    
    def importCastsData(self):
        conn = self.conn
        casts = pd.read_sql("Select FILM_ID, CAST_MEMBER, CAST_ROLE FROM RELMDB.CASTS", conn)
        #casts.head()
        return casts
    
    def importTagsData(self):
        conn = self.conn
        tags = pd.read_sql("Select FAN_ID, USER_SPECIFIC_TAGS, TIMESTAMP FROM TAGS", conn)
        #casts.head()
        return tags
    
    #Merging dataframes
    def mergeMovieData(self):
        users_data = self.importUsersData()
        movies = self.importMoviesData()
        genres = self.importGenresData()
        directors = self.importDirectorsData()
        casts = self.importCastsData()
        user_specific_tags = self.importTagsData()
        
        users_tags_data = pd.merge(users_data, user_specific_tags, on = "FAN_ID")
        movie_user_data = pd.merge(users_tags_data, movies, on = "FILM_ID")
        director_cast_data = pd.merge(directors, casts, on = "FILM_ID")
        movie_user_genre_data = pd.merge(movie_user_data, genres, on = "FILM_ID")
        movie_detailed_data = pd.merge(movie_user_genre_data, director_cast_data, on = "FILM_ID")
        
        return movie_detailed_data