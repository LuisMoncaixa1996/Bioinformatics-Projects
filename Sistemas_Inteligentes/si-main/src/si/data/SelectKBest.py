import numpy as np
from.dataset import Dataset
from copy import copy
import warnings
import scipy.stats as stats
from ..util import f_anova

class SelectKBest:

    def __init__(self,k, func = f_anova):
        if k > 0:
            self.k = k
        else:
            raise Exception('K-value must be > 0!')
        self.func = func

    def fit(self,dataset):
        """ Aplica o teste estatistico selecionado ao dataset, obtendo os valores de p-value e F-score."""
        self.F_value,self.p_value = self.func(dataset)

    def transform(self,dataset,inline=False):
        '''Inicialmente, a partir dos valores de F-score obtidos, estes serão ordenados de forma a que os k
        F-scores sejam os maiores. De seguida é filtrado o dataset consoante esses valores de F-score.
        Gerando assim um novo dataset com os dados filtrados.
        '''
        X = dataset.X
        K_Best = np.argsort(self.F_value)[-self.k :]
        New_X = X[:, K_Best]
        columns = []
        for i in K_Best:
            columns.append(dataset._xnames[i])
        if inline:
            dataset.X = New_X
            dataset._xnames = columns
            return dataset
        else:
            return Dataset(New_X, copy(dataset.Y), columns, copy(dataset._yname))

    
    def fit_transform(self,dataset, inline = False):
        self.fit(dataset)
        return self.transform(dataset, inline=inline)



