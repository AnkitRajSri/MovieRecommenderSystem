from surprise.model_selection import train_test_split
from surprise.model_selection import LeaveOneOut
from surprise import KNNBaseline

class EvaluationData:
    
    def __init__(self, data, popularityRanks):
        self.rankings = popularityRanks
        
        #Build a full training set for evaluating the overall properties
        self.fullTrainSet = data.build_full_trainset()
        self.fullAntiTestSet = data.fullTrainSet.build_anti_testset()
        
        #Build a 70/30 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(data, test_size = 0.30, random_state = 1)
        
        
        def getFullTrainSet(self):
            return self.fullTrainSet
        
        def getFullAntiTestSet(self):
            return self.fullAntiTestSet
        
        def GetTrainSet(self):
            return self.trainSet
    
        def GetTestSet(self):
            return self.testSet

