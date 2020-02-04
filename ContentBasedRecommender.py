#Importing libraries
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class ContentBasedRecommender:
    
    def __init__(self, moviesData):
        self.moviesData = moviesData
        
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
        highest_rating = movies_ratings["MEAN_RATING"].max()
        best_movie = movies_ratings[movies_ratings["MEAN_RATING"] == highest_rating]["FILM_ID"].values
        highest_rated_movie = movies_detailed_data[movies_detailed_data["FILM_ID"] == best_movie[0]].drop(["IMDB_RATING", "CAST_ROLE"], axis = 1)
        return highest_rated_movie
    
    #Merging the key features in a single column
    def mergeKeyFeatures(self):
        moviesData = self.moviesData
        movies_detailed_data = moviesData.mergeMovieData()
        movies_key_data = movies_detailed_data.assign(Key_Features = movies_detailed_data.FILM_YEAR.astype(str) + " " +\
                                          movies_detailed_data.IMDB_VOTES.astype(str) + " "+\
                                          movies_detailed_data.GENRE.astype(str) + " " +\
                                          movies_detailed_data.DIRECTOR.astype(str) + " " +\
                                          movies_detailed_data.CAST_MEMBER.astype(str) + " " +\
                                          movies_detailed_data.CAST_ROLE.astype(str) + " " +\
                                          movies_detailed_data.USER_SPECIFIC_TAGS.astype(str)).drop(["FAN_ID",\
                                                                               "FILM_ID", "IMDB_RATING", "CAST_ROLE",\
                                                                               "FILM_YEAR","IMDB_VOTES","GENRE",\
                                                                               "DIRECTOR","CAST_MEMBER", \
                                                                               "USER_SPECIFIC_TAGS"], axis = 1)
  
        movies_key_data = movies_key_data.drop_duplicates(["FILM_TITLE"]).set_index("FILM_TITLE")
        movies_key_data.index.names = ["FILM_TITLE"]
        return movies_key_data
    
    #Building cosine similarity matrix
    def buildCosineSimilarity(self):
        movies_key_data = self.mergeKeyFeatures()
        count = CountVectorizer()
        count_matrix = count.fit_transform(movies_key_data["Key_Features"])

        cosine_sim_matrix = cosine_similarity(count_matrix, count_matrix)
        return cosine_sim_matrix
    
    #Generating content based recommendations
    def generateRecommendations(self):
        cosine_sim_matrix = self.buildCosineSimilarity()
        movies_key_data = self.mergeKeyFeatures()
        highest_rated_movie = self.getMovieDetails()
        highest_rated_movie_name = highest_rated_movie["FILM_TITLE"].unique()
        
        #Creating a list to match the indices
        movies_indices = pd.Series(movies_key_data.index)

        recommended_movies = []
        
        #Getting the index of the movie that matches title of the highest rated movie
        idx = movies_indices[movies_indices == highest_rated_movie_name[0]].index[0]

        #Creating a series with the similarity scores in the descending order
        sim_score_series = pd.Series(cosine_sim_matrix[idx]).sort_values(ascending = False)

        #Getting the indices of top 10 most similar movies
        top_10 = list(sim_score_series.iloc[1:11].index)

        #Populating the recommended movies list with the titles of top 10 matching movies
        for i in top_10:
            recommended_movies.append(list(movies_key_data.index)[i])
            
        return recommended_movies
 