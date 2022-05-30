import itertools
import numpy as np

# Y is reserved to idenfify dependent variables
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXZ'

__all__ = ['label_gen', 'mse','f_anova', 'euclidean', 'accuracy_score', 'add_intersect', 'train_test_split','_sigmoid','to_categorical']


def label_gen(n):
    """ Generates a list of n distinct labels similar to Excel"""
    def _iter_all_strings():
        size = 1
        while True:
            for s in itertools.product(ALPHA, repeat=size):
                yield "".join(s)
            size += 1

    generator = _iter_all_strings()

    def gen():
        for s in generator:
            return s

    return [gen() for _ in range(n)]


def train_test_split(dataset,split= 0.8):
    n = dataset.X.shape[0]
    m = int(split*n)
    arr = np.arange(n)
    np.random.shuffle(arr)
    from ..data import Dataset
    train = Dataset(dataset.X[arr[:m]],dataset.Y[arr[:m]], dataset._xnames, dataset._yname)
    test = Dataset(dataset.X[arr[m:]],dataset.Y[arr[m:]], dataset._xnames, dataset._yname)
    return train, test


def accuracy_score(y_true,y_pred):
        correct = 0
        for true, pred in zip(y_true,y_pred):
            if true == pred:
                correct +=1
        accuracy = correct / len(y_true)
        return accuracy

def euclidean(x,y):
    return np.sqrt(np.sum((x - y)**2, axis=1))


def f_anova(dataset):
    X,Y = dataset.getXy()
    values = []
    for k in np.unique(Y):
        values.append(X[Y == k,:])
    from scipy.stats import f_oneway
    F_value, p_value = f_oneway(*values )
    return F_value, p_value


def mse(y_true,y_pred,squared=True):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    errors = np.average((y_true - y_pred)**2, axis=0)
    if not squared:
        errors = np.sqrt(errors)
    return np.average(errors)


def _sigmoid(x):
        return 1 / (1 + np.exp(-x))

def add_intersect(X):
    return np.hstack((np.ones((X.shape[0],1)),X))

def to_categorical(y, num_classes=None, dtype='float32'):
    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


def minibatch(X, batchsize=256, shuffle=True):
    N = X.shape[0]
    ix = np.arange(N)
    n_batches = int(np.ceil(N / batchsize))

    if shuffle:
        np.random.shuffle(ix)

    def mb_generator():
        for i in range(n_batches):
            yield ix[i * batchsize: (i + 1) * batchsize]

    return mb_generator()