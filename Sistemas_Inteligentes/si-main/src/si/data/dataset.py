import numpy as np
import pandas as pd
from ..util import label_gen

__all__ = ['Dataset']


class Dataset:
    def __init__(self, X=None, Y=None,
                 xnames: list = None,
                 yname: str = None):
        """ Tabular Dataset"""
        if X is None:
            raise Exception("Trying to instanciate a DataSet without any data")
        self.X = X
        self.Y = Y
        self._xnames = xnames if xnames else label_gen(X.shape[1])
        self._yname = yname if yname else 'Y'

    @classmethod
    def from_data(cls, filename, sep=",", labeled=True):
        """Creates a DataSet from a data file.

        :param filename: The filename
        :type filename: str
        :param sep: attributes separator, defaults to ","
        :type sep: str, optional
        :return: A DataSet object
        :rtype: DataSet
        """

        data = np.genfromtxt(filename, delimiter=sep)
        if labeled:
            X = data[:, 0:-1]
            Y = data[:, -1]
        else:
            X = data
            Y = None
        return cls(X, Y)

    @classmethod
    def from_dataframe(cls, df, ylabel=None):
        """Creates a DataSet from a pandas dataframe.

        :param df: [description]
        :type df: [type]
        :param ylabel: [description], defaults to None
        :type ylabel: [type], optional
        :return: [description]
        :rtype: [type]
        """
        if ylabel is not None and ylabel in df.columns:
            X = df.loc[:, df.columns != ylabel].to_numpy()
            Y = df.loc[:, df.columns == ylabel].to_numpy()
            xnames = df.columns.tolist().remove(ylabel)
            yname = ylabel

        else:
            X = df.to_numpy() #Coverte o dataset em numpy
            Y = None
            xnames = df.columns.tolist() #Nomes em uma lista a partir do numpy
            yname = None    
        return (cls(X,Y,xnames,yname))

    def __len__(self):
        """Returns the number of data points.""" #Numero de linhas
        return self.X.shape[0]

    def hasLabel(self):
        """Returns True if the dataset constains labels (a dependent variable)"""
        if self.Y is not None:
            return True
        else:
            return False

    def getNumFeatures(self): #Numero de colunas
        """Returns the number of features"""
        return self.X.shape[1]

    def getNumClasses(self):
        """Returns the number of label classes or 0 if the dataset has no dependent variable."""
        if self.hasLabel():
            return len(np.unique(self.Y))
        else:
            return 0
    

    def writeDataset(self, filename, sep=","):
        """Saves the dataset to a file

        :param filename: The output file path
        :type filename: str
        :param sep: The fields separator, defaults to ","
        :type sep: str, optional
        """

        fullds = np.hstack((self.X, self.Y.reshape(len(self.Y), 1)))
        np.savetxt(filename, fullds, delimiter=sep)

    def toDataframe(self):
        """ Converts the dataset into a pandas DataFrame"""
        if self.Y is not None:
            fullds = np.hstack((self.X, self.Y.reshape(len(self.Y), 1)))
            columns = np.hstack((self._xnames, self._yname))
        else:
            fullds = self.X.copy()
            columns = self._xnames[:]
        return pd.DataFrame(fullds, columns=columns)

    def getXy(self):
        return self.X, self.Y

def summary(dataset, format='df'):
    """ Returns the statistics of a dataset(mean, std, max, min)

    :param dataset: A Dataset object
    :type dataset: si.data.Dataset
    :param format: Output format ('df':DataFrame, 'dict':dictionary ), defaults to 'df'
    :type format: str, optional
    """
    if dataset.hasLabel():
        idx = np.hstack((dataset.X, dataset.Y.reshape(len(dataset.Y), 1)))
        columns = dataset._xnames[:]+[dataset._yname]
    else:
        idx = dataset.X.copy()
        columns = dataset._xnames[:]
    values = {}
    for i in range(idx.shape[1]):
        value = {
            'mean' : np.mean(idx[:,i],axis=0),
            'var': np.var(idx[:,i],axis= 0),
            'max': np.max(idx[:,i],axis=0),
            'min': np.min(idx[:,i],axis=0)
        }
        values[columns[i]]= value
    if format == 'df':
        df= pd.DataFrame(values)
        return df
    else:
        return values