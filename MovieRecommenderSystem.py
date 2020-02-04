
from OracleDBConnection import OracleDBConnection
from HybridRecommender import HybridRecommenderSystem
from MoviesData import MoviesData
from UserBasedRecommender import UserBasedRecommender
from ContentBasedRecommender import ContentBasedRecommender


class RecommenderInterface:
    
    def main():
        ip = "131.247.223.52"
        port = 1521
        SID = "cdb9"
        user_name = "DB511"
        password = "db5pass"

        oracleDBConnection = OracleDBConnection(ip, port, SID, user_name, password)
        conn = oracleDBConnection.createConnection()
    
        moviesData = MoviesData(conn)
        userBasedRecommendations = UserBasedRecommender(moviesData)
        contentBasedRecommendations = ContentBasedRecommender(moviesData)
        hybridRecommender = HybridRecommenderSystem(moviesData, userBasedRecommendations, contentBasedRecommendations)
        hybridRecommender.displayContentBasedRecommendations()
        hybridRecommender.displayUserBasedRecommendations()
        
    if __name__ == "main":
        main()
        