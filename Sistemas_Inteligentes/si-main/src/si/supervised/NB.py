import numpy as np


class Naive_Bayes:


    def fit(self,dataset):

        self.classes = np.unique(dataset.Y)
        self.rows = dataset.X.shape[0]
        

