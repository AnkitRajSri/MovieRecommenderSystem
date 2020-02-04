class HybridRecommenderSystem:
    
    def __init__(self, moviesData, userBasedRecommendations, contentBasedRecommendations):
        self.moviesData = moviesData
        self.userBasedRecommendations = userBasedRecommendations
        self.contentBasedRecommendations = contentBasedRecommendations
    
    def displayContentBasedRecommendations(self):
        recommended_movies = self.contentBasedRecommendations.generateRecommendations()
        print("\n Based on similar content, we recommend: ")
        count = 0
        for i in recommended_movies:
            count = count+1
            print(count,i)
            
    def displayUserBasedRecommendations(self):
        recommendedMovies = self.userBasedRecommendations.generateMovieRecommendations()
        print("Checking")
        print("\n Based on user behaviour, we recommend: ")
        count = 0
        for i in recommendedMovies:
            count = count+1
            print(count,i)
        