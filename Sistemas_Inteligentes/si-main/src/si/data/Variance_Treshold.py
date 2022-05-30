import numpy as np
from scipy.stats import stats
from copy import copy
import warnings

class VarianceThreshold:
    def __init__(self, threshold = 0):
        if threshold < 0:
            warnings.warn("The treshold must be non-negative value")
        self.treshold = threshold

    def fit(self,dataset):
        X = dataset.X
        self._var = np.var(X,axis = 0)
    
    def transform(self, dataset, inline = False):
        """Verifica se as variâncias dos valores são superiores ao treshold indicado
            e filtra o dataset nos dados em que isso se confirma, através do indice, atualizando por
            fim o dataset com os valores cujo a variância é maior que o treshold e os respetivos nomes.
            """
        X = dataset.X
        cond = self._var > self.treshold
        index = []
        for i in range(len(cond)):
            if cond[i]:
                 index.append(i)
        X_trans = X[:,index]
        xnames = []
        for i in index:
            xnames.append(dataset._xnames[i])
        if inline:
            dataset.X = X_trans
            dataset._xnames = xnames
            return dataset
        else:
            from.dataset import Dataset
            return Dataset(X_trans, copy(dataset.Y), xnames,copy(dataset._yname))
            
    def fit_transform(self, dataset, inline=False):
        """
        Calculate and store the mean and variance of each feature and
        standardize the data.
        Parameters
        ----------
        dataset : A Dataset object to be standardized
        Returns
        -------
        A Dataset object to with standardized data.
        """
        self.fit(dataset)
        return self.transform(dataset, inline=inline)
