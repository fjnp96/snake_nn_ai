import menu
import config
from neural_network import *
fps = 10

def main(menu):
    print("Hello world")
    if(not config.skip_menu):
        mainMenu = menu.Menu(800,600)
        mainMenu.display()
    train()

def train():
    population = generate_population(config.training_population)
    for i in population:
        game = Game()

def generate_population(x):
    population = []
    layers = config.nn_nb_hidden_layers
    activation_function = get_activation_function()
    for i in range(x):
        nn = Network(i)
        #add first layer based on number of inputs
        nn.add(FCLayer(config.nn_nb_inputs,layers[0]))
        nn.add(ActivationLayer(activation_function))
        for j in range(1,len(layers)):
            nn.add(FCLayer(layers[j-1],layers[j]))
            nn.add(ActivationLayer(activation_function))
        #add Output Layer
        nn.add(FCLayer(layers[len(layers)-1],3))
        nn.add(ActivationLayer(lambda a : a))
        population.append(nn)
    return population

def equal(x):
    return x

if __name__ == "__main__":
    main(menu)

