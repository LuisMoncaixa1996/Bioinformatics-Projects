import numpy as np
from ..util.util import euclidean
import warnings


class Kmeans:
    def __init__(self, k :int, itera = 1000, dist = 'euclidean'):
        self.k = k
        self.itera = itera
        if dist == 'euclidean':
            self.dist = euclidean
        else:
            raise Exception('Distance metric not available \n Score functions: euclidean, manhattan')

    def fit(self,dataset):
        X = dataset.X
        self.min = np.min(X,axis = 0)
        self.max = np.max(X, axis = 0)

    def init_centroids(self, dataset):
        '''Seleção aleatória dos primeiros k clusters '''
        X = dataset.X
        idx = np.random.choice(X.shape[0],self.k,replace = False)
        for i in idx:
            self.centroids = X[idx]
        print(self.centroids)

    def closest_centroid(self,x):
        '''Cálculo dos restantes clusters em relação aos primeiros selecionados aleatóriamente e 
        através do cálculo das distâncias verifica a qual cluster estes se encontram mais proximos. '''
        dist = euclidean(x,self.centroids)
        closest_centroid_ind = np.argmin(dist,axis = 0)
        return closest_centroid_ind

    def fit_transform(self,dataset):
        self.fit(dataset)
        centroides, idxs = self.transform(dataset)
        return centroides, idxs

    def transform(self,dataset):
        '''A partir da escolha inicial dos k clusters, irá se verificar a proximidade de todos os dados do dataset
        a esses k cluster escolhidos aletóriamente gerando os seus indíces. Posteriormente será calculada a média
        desses desses pontos nos indices obtidos e verificar os clusters centrais. Após não existir alteração nos
        indices estes serão guardados assim como os clusters centrais.'''
        self.init_centroids(dataset)
        print(self.centroids)
        X = dataset.X
        change = True
        count = 0
        old_ind = np.zeros(X.shape[0])
        while change and count < self.itera:
            idxs = np.apply_along_axis(self.closest_centroid,axis = 0, arr = X.T)
            cent = []
            for i in range(self.k):
                cent.append(np.mean(X[idxs == i], axis = 0))
            self.centroids = np.array(cent)
            if np.any(old_ind == idxs):
                change = False
            old_ind = idxs
            count += 1
        return self.centroids,idxs