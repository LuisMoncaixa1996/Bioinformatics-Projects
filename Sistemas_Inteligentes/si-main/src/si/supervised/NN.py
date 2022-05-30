from abc import abstractmethod, ABC
from typing import MutableSequence
from .model import Model
from scipy import signal
import numpy as np
from ..util.metrics import mse, mse_prime
from ..util.im2col import col2im,im2col,pad2D


class Layer(ABC):
    

    def __init__(self):
        super().__init__()
        self.input = None
        self.output = None
    
    @abstractmethod
    def forward(self,input):
        raise NotImplementedError
    
    @abstractmethod
    def backward(self,output_error,learning_rate):
        raise NotImplementedError
    
class Dense(Layer):

    def __init__(self, input_size, output_size):
        "Fully connected layer"
        self.weights = np.random.rand(input_size,output_size) - 0.5
        self.bias = np.zeros((1,output_size))

    def setWeights(self, weights, bias):
        """ Sets the weights for the NN.
        :param weights: An numpy.array of weights
        : param bias: the numpy array of bias weights
        """
        if(weights.shape != self.weights.shape):
            raise ValueError(f"Shapes mismatch {weights.shape} and ")
        if(bias.shape != self.bias.shape):
            raise ValueError(f"Shapes mismatch {bias.shape} and ")
        self.weights = weights
        self.bias = bias


    def forward(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output


    def backward(self, output_Error, learning_rate):
        """Computes dE/dW, dE/dB for a given output_error = dE/dY.
        Returns input_error = dE/dX to feed the previous layer. """
        #compute the weights error dE/dW = X.T * dE/dY
        weights_error = np.dot(self.input.T, output_Error)
        #compute the bias error dE/dB = dE/dY
        bias_error = np.sum(output_Error, axis=0)
        #error dE/dX to pass on to the previous layer
        input_error = np.dot(output_Error, self.weights.T)
        #update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * bias_error
        return input_error


class activation(Layer):

    def __init__(self,activation):
        self.activation = activation
    
    def forward (self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output
    
    def backward ( self, output_error, learning_rate):
        #learning_rate is not used because there is no "learnable" parameters.
        #Only passed the error do the previous layer
        return np.multiply(self.activation.prime(self.input), output_error)


class NN(Model):

    def __init__(self, epochs = 1000, lr = 0.001, verbose = True):
        super().__init__()

        self.epochs = epochs
        self.lr = lr
        self.verbose = verbose

        self.layers = []
        self.loss = mse
        self.loss_prime = mse_prime
    
    def add(self,layer):
        self.layers.append(layer)
    
    def fit(self,dataset):
        X,y = dataset.getXy()
        self.dataset = dataset
        self.history = dict()
        for epoch in range(self.epochs):
            output = X
            #foward propagation
            for layer in self.layers:
                output = layer.forward(output)
            
            #backward propagation
            error = self.loss_prime(y, output)
            for layer in reversed(self.layers):
                error = layer.backward(error, self.lr)
            
            #calculate average error on all samples
            err = self.loss(y,output)
            self.history[epoch] = err
            if self.verbose:
                print(f'epoch{epoch+1}/{self.epoch} error = {err}')
        
        if not self.verbose:
            print(f'error = {err}')
        self.is_fitted = True
    
    def predict(self,input_data):
        assert self.is_fitted, "Model must be fit before predict"
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def cost(self, X=None, y=None):
        assert self.is_fitted, "Model must be fit before predict"
        X = X if X is not None else self.dataset.X
        y = y if y is not None else self.dataset.y
        output = self.predict(X)
        return self.loss(y, output)



class Flatten(Layer):

    def forward(self,input):
        self.input_shape = input.shape
        # flattens all  but the 1st dimention
        output = input.reshape(input.shape[0], -1)
        return output
    
    def backward(self,output_error,learning_rate):
        return output_error.reshape(self.input_shape)

class Conv2D(Layer):

    def __init__(self,input_shape, kernel_shape,layer_depth, stride =1, padding = 0):
        self.input_shape = input_shape
        self.in_ch = input_shape[2]
        self.out_ch = layer_depth
        self.stride = stride
        self.padding = padding

        #weights
        self.weights = np.random.rand(kernel_shape[0], kernel_shape[1],
                                    self.in_ch, self.out_ch) - 0.5
        #bias
        self.bias = np.zeros((self.out_ch,1))
    
    def forward(self, input_data):
        s = self.stride
        self.X_shape = input_data.shape
        _, p = pad2D(input_data, self.padding, self.weights.shape[:2],s)

        pr1, pr2, pc1, pc2 = p
        fr, fc, in_ch, out_ch = self.weights.shape
        n_ex, in_rows, in_cols, in_ch = input_data.shape

        # compute the dimensions of the convolution output
        out_rows = int((in_rows + pr1 + pr2 - fr)/ s+1)
        out_cols = int((in_cols + pc1 + pc2 - fc)/s+1)

        #convert X and W inte the appropriate 2D matrices and take their product 

        self.X_col, _ = im2col(input_data, self.weights.shape, p,s)
        W_col = self.weights.transpose(3,2,0,1).reshape(out_ch, -1)

        output_data = (W_col @ self.X_col + self.bias).reshape(out_ch, out_rows, out_cols, n_ex).transpose(3,1,2,0)

        return output_data

    def backward(self, output_error, learning_rate):

        fr, fc, in_ch, out_ch = self.weights.shape
        p = self.padding

        db = np.sum(output_error, axis = (0,1,2))
        db = db.reshape(out_ch,)

        dout_reshaped = output_error.transpose(1,2,3,0).reshape(out_ch,-1)
        dW = dout_reshaped @ self.X_col.T
        dW = dW.reshape(self.weights.shape)

        W_reshape = self.weights.reshape(out_ch, -1)
        dX_col = W_reshape.T @ dout_reshaped
        input_error = col2im(dX_col, self.X_shape, self.weights.shape, (p,p,p,p), self.stride)

        self.weights -= learning_rate*dW
        self.bias -= learning_rate*db

        return input_error



class Pooling2D(Layer):

    def __init__(self, size=2, stride= 2):
        self.size = size
        self.stride = stride

    def pool(X_col):
        mean_idx = np.mean(X_col, axis=0)
        out = X_col[mean_idx, range(mean_idx.size)]
        return out, mean_idx

    def dpool(dX_col, dout_col, pool_cache):
        pass


    def forward(self,input):
        self.X_shape = input.shape
        n,h,w,d = input.shape
        h_out = (h - self.size) / self.stride + 1
        w_out = (w - self.size) / self.stride + 1

        if not w_out.is_integer() or not h_out.is_integer():
            raise Exception("Invalid output dimension")
        h_out, w_out = int(h_out), int(w_out)
        X = input.transpose(0,3,1,2)
        X_reshaped = input.reshape(n*d,h,w,1)
        self.X_col,l = im2col(X_reshaped,  (self.size, self.size,d,d), pad = 0, stride = self.stride)
        print(self.X_col)


        out, self.max_idx = self.pool(self.X_col)

        out = out.reshape(d,h_out, w_out, n)
        out = out.transpose(3,1,2,0)

        return out
    
    def backward(self, output_error, learning_rate):
        n,w,h,d = self.X_shape
        dX_col = np.zeros_like(self.X_col)
        dout_col = output_error.transpose(1,2,3,0).ravel()

        dX = self.dpool(dX_col, dout_col, self.max_idx)
        dX = col2im(dX_col,(n*d,h,w,1), (self.size,self.size,d,d),padding=0,stride = self.stride)

        dX = dX.reshape(self.X_shape)
        return dX

class MaxPooling2D(Pooling2D):

    def pool(X_col):
        max_idx = np.argmax(X_col, axis=0)
        out = X_col[max_idx, range(max_idx.size)]
        return out, max_idx

    def dpool(dX_col, dout_col, pool_cache):
        dX_col[pool_cache, range(dout_col.size)] = dout_col
        return dX_col