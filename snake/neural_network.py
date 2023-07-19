import numpy as np

class Network:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)
    def predict(self, input_data):
        samples = len(input_data)
        result = []

        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)
        return result

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagation(self,input):
        raise NotImplementedError

class FCLayer(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size,output_size) - 0.50
        self.bias = np.random.rand(1,output_size) - 0.5

    def forward_propagation(self,input_data):
        self.input = input_data
        self.output = np.dot(self.input,self.weights) + self.bias
        return self.output

class ActivationLayer(Layer):
    def __init__(self, activation):
        self.activation = activation

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

def tanh(x):
     return np.tanh(x)
