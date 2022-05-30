import numpy as np
from numpy.core.numeric import identity
from src.si.data import Dataset
from si.supervised.model import Model
from ..util import mse, add_intersect, _sigmoid


class LogisticRegression():

    def __init__(self, gd=False, epochs=1000, lr=0.001):
        super(LogisticRegression, self).__init__()
        self.gd = gd
        self.theta = None
        self.epochs = epochs
        self.lr = lr

    def fit(self, dataset):
        x, y = dataset.getXy()
        x = np.hstack((np.ones((x.shape[0], 1)), x))
        self.X = x
        self.Y = y
        self.train(x, y)
        self.is_fitted = True


    def train(self, X, y):
        m = X.shape[0]
        n = X.shape[1]
        self.history = {}
        self.theta = np.zeros(n)
        for epoch in range(self.epochs):
            A = self.X.dot(self.theta)
            B = _sigmoid(A)
            tmp = B - self.Y.T
            #tmp = np.reshape(tmp,m)
            dW = np.dot(self.X.T, tmp) / m
            self.theta -= self.lr * dW
            self.history[epoch] = [self.theta[:], self.cost()]

    def predict(self, x):
        assert self.is_fitted, 'Model must be fit before predicting'
        __x = np.hstack(([1], x))
        Z = _sigmoid(np.dot(self.theta, __x))
        res = np.where(Z > 0.5,1,0)
        return res

    def cost(self, X=None, Y=None, theta=None):
        X = add_intersect(X) if X is not None else self.X
        y = Y if Y is not None else self.Y
        theta = theta if theta is not None else self.theta
        y_pred = _sigmoid(np.dot(self.X, self.theta))
        return (sum((self.Y)*np.log(y_pred) + (1-self.Y)*np.log(1-y_pred))) / (-self.X.shape[0])


class LogisticRegressionReg(LogisticRegression):

    def __init__(self, gd=False, epochs=1000, lr=0.001, lbd=1):
        super(LogisticRegressionReg, self).__init__(gd=gd, epochs=epochs, lr=lr)
        self.lbd = lbd


    def train(self, X, y):
        m = X.shape[0]
        n = X.shape[1]
        self.history = {}
        self.theta = np.zeros(n)
        lbds = np.full(m, self.lbd)
        lbds[0] = 0
        for epoch in range(self.epochs):
            A = _sigmoid(self.X.dot(self.theta))
            tmp = A - self.Y.T
            dW = np.dot(self.X.T, tmp) / y.size
            dW[1:] = dW[1:] + (self.lbd / m) * self.theta[1:]
            self.theta -= self.lr * dW
            self.history[epoch] = [self.theta[:], self.cost()]

    def cost(self, X=None, Y=None, theta=None):
        X = add_intersect(X) if X is not None else self.X
        y = Y if Y is not None else self.Y
        theta = theta if theta is not None else self.theta
        y_pred = _sigmoid(np.dot(self.X, self.theta))
        reg = np.dot(theta[1:], theta[1:]) * self.lbd / (2 * self.X.shape[0])
        cost = (sum((self.Y)*np.log(y_pred) + (1-self.Y)*np.log(1-y_pred))) / (-self.X.shape[0])
        return cost + reg