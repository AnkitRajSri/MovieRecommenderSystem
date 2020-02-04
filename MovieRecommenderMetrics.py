import itertools

from surprise import accuracy
from collections import defaultdict

class RecommenderPerformanceMetrics:
    
    def MAE(predictions):
        return accuracy.mae(predictions, verbose = False)
    
    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose = False)
    

