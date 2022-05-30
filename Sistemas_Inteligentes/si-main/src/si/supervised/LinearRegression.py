import numpy as np
from numpy.core.numeric import identity
from ..data import Dataset
from ..util import mse, add_intersect



class LinearRegression:

    def __init__(self, gd=False,epochs = 1000, lr = 0.001):
        super(LinearRegression,self).__init__()
        self.gd = gd
        self.theta = None
        self.epochs = epochs
        self.lr = lr
    
    def fit(self,dataset):
        x,y = dataset.getXy()
        x = np.hstack((np.ones((x.shape[0],1)),x))
        self.X = x
        self.Y = y
        self.train_gd(x,y) if self.gd else self.train_closed(x,y)
        self.is_fitted = True
        
    def train_closed(self,X,y):
        self.theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    def train_gd(self,X,y):
        m = X.shape[0]
        n = X.shape[1]
        self.history = {}
        self.theta = np.zeros(n)
        for epoch in range(self.epochs):
            grad = 1/m * (X.dot(self.theta)-y).dot(X)
            self.theta -= self.lr * grad
            self.history[epoch] = [self.theta[:], self.cost()]


    def predict(self,x):
        assert self.is_fitted, 'Model must be fit before predicting'
        __x = np.hstack(([1],x))
        return np.dot(self.theta, __x)


    def cost(self, X = None, Y=None, theta = None):
        X = add_intersect(X) if X is not None else self.X
        y = Y if Y is not None else self.Y
        theta = theta if theta is not None else self.theta
        y_pred = np.dot(X, theta)
        return mse(y,y_pred)/2



class LinearRegressionReg(LinearRegression):

    def __init__(self, gd=False, epochs=1000, lr=0.001, lbd=1):
        super(LinearRegressionReg, self).__init__(gd=gd, epochs=epochs, lr=lr)
        self.lbd = lbd


    def train_closed(self, X, y):
        n = X.shape[1]
        identity = np.eye(n)
        identity[0,0] = 0
        self.theta = np.linalg.inv(X.T.dot(X)+self.lbd*identity).dot(X.T).dot(y)
        self.is_fitted = True
    
    def train_gd(self, X, y):
        m = X.shape[0]
        n = X.shape[1]
        self.history = {}
        self.theta = np.zeros(n)
        lbds = np.full(m,self.lbd)
        lbds[0] = 0
        for epoch in range(self.epochs):
            grad = (X.dot(self.theta)-y).dot(X)
            self.theta -= (self.lr/m) * (lbds+grad)
            self.history[epoch] = [self.theta[:], self.cost(X,y)]
