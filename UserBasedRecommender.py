#Importing libraries

import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD

class UserBasedRecommender:
    
    def __init__(self, moviesData, n_components = 12, random_state = 17):
        self.moviesData = moviesData
        self.n_components = n_components
        self.random_state = random_state
        
    #Identifying movies with the highest average rating
    def identifyHighestRatedMovies(self):
        moviesData = self.moviesData
        movies_detailed_data = moviesData.mergeMovieData()
        movies_detailed_data = movies_detailed_data.sort_values(by = "IMDB_VOTES", ascending = False)
        movie_ratings = movies_detailed_data.groupby("FILM_ID")["IMDB_RATING"].mean().to_frame("MEAN_RATING").reset_index()
        #movie_ratings.head()
        return movie_ratings

    #Getting the details of the highest average rated movie
    def getMovieDetails(self):
        moviesData = self.moviesData
        movies_detailed_data = moviesData.mergeMovieData()
        movies_ratings = self.identifyHighestRatedMovies()
        movies_detailed_data = pd.merge(movies_detailed_data, movies_ratings, on = "FILM_ID").drop_duplicates(["FAN_ID", "FILM_ID"])
        highest_rating = movies_ratings["MEAN_RATING"].max()
        best_movie = movies_ratings[movies_ratings["MEAN_RATING"] == highest_rating]["FILM_ID"].values
        highest_rated_movie = movies_detailed_data[movies_detailed_data["FILM_ID"] == best_movie[0]].drop(["IMDB_RATING", "CAST_ROLE"], axis = 1)
        
        highest_rated_movie_name = highest_rated_movie["FILM_TITLE"].unique().astype(str)
        return highest_rated_movie_name
    
    #Building a utility matrix for each user and each movie
    def buildUtilityMatix(self):
        moviesData = self.moviesData
        movies_detailed_data = moviesData.mergeMovieData()
        ratings_pivot = movies_detailed_data.pivot_table(values = "IMDB_RATING", index = "FAN_ID", columns = "FILM_TITLE", fill_value = 0)
        print(ratings_pivot.shape)
        return ratings_pivot
     
    #Buiding a decomposition matrix
    def decomposeMoviesData(self):
        ratings_pivot = self.buildUtilityMatix()
        transposed_pivot = ratings_pivot.values.T
        SVD = TruncatedSVD(n_components = self.n_components, random_state = self.random_state)
        resultant_matrix = SVD.fit_transform(transposed_pivot)
        resultant_matrix.shape
        
        return resultant_matrix

    #Generating movie recommendations based on user behaviour
    def generateMovieRecommendations(self):
        #Generating a Correlation Matrix
        ratings_pivot = self.buildUtilityMatix()
        final_data_matrix = self.decomposeMoviesData()
        highest_rated_movie = self.getMovieDetails()
        corr_mat = np.corrcoef(final_data_matrix)
        corr_mat.shape

        #Isolating Most rated movie from the Correlation Matrix
        movies_names = ratings_pivot.columns
        movies_names
        movies_list = list(movies_names)
        movies_list
        movie_res = movies_list.index(highest_rated_movie[0])
        print(movie_res)

        corr_movie_res = corr_mat[movie_res]
        corr_movie_res.shape

        #Recommending a Highly Correlated Movie
        recommendedMovies = list(movies_names[(corr_movie_res < 1.0) & (corr_movie_res > 0.4)])
        return recommendedMovies