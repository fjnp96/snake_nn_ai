import numpy as np
import random
import config

class Network:
    def __init__(self,nn_id=None):
        self.id = nn_id
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    """
    #Usual predict for each sample we dont want this
    def predict(self, input_data):
        samples = len(input_data)
        result = []

        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)
        return result
    """
    def predict(self, input_data):
        output = input_data
        for layer in self.layers:
            output = layer.forward_propagation(output)
        return output[0]

    def mutate(self,prob=config.default_mutation_rate):
        for layer in self.layers:
            if(not isinstance(layer,FCLayer)):
                continue
            layer.weights += mutate_matrix(np.shape(layer.weights),prob)
            layer.bias += mutate_matrix(np.shape(layer.bias),prob)

    def random_crossover(self,parent2,child_id=None):
        child = Network(child_id)
        for (layer1,layer2) in zip(self.layers, parent2.layers):
            if(not isinstance(layer1,FCLayer)):
                child.add(ActivationLayer(layer1.activation))
                continue
            shape = np.shape(layer1.weights)
            child_layer=FCLayer(shape[0],shape[1])
            crossover_bool_matrix = np.random.choice(a=[True, False], size=shape, p=[0.5, 0.5])
            child_layer.weights = np.where(crossover_bool_matrix,layer1.weights,layer2.weights)
            crossover_bool_matrix = np.random.choice(a=[True, False], size=np.shape(layer1.bias), p=[0.5, 0.5])
            child_layer.bias = np.where(crossover_bool_matrix,layer1.bias,layer2.bias)
            child.add(child_layer)
        return child




    def print(self):
        print("Printing Network")
        print("NN ID: ",self.id)
        for i in range(len(self.layers)):
            if(isinstance(self.layers[i],FCLayer)):
                print("//// FCLayer"+str(i+1)+" ////")
                print("Weights")
                print(self.layers[i].weights)
                print("Bias")
                print(self.layers[i].bias)
            if(isinstance(self.layers[i], ActivationLayer)):
                print("//// ActivationLayer"+str(i+1)+" ////")
                print("Activation Function: "+self.layers[i].activation.__name__)

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

def get_activation_function():
    if(config.activation_function == "tahn"):
        return tanh

def tanh(x):
     return np.tanh(x)

#Returns a Matrix to be summed to the NN matrix changing the values of the actual layer
def mutate_matrix(shape,prob):
    mutate_value_matrix = np.random.uniform(config.min_mutation,config.max_mutation,size = shape)
    mutate_bool_matrix = np.random.choice(a=[True, False], size=shape, p=[prob, 1-prob])
    zero_matrix = np.zeros(shape)
    return np.where(mutate_bool_matrix,mutate_value_matrix,zero_matrix)

