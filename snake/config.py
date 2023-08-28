#Config file
#Genetic Type
#0 -> New population = Top performers + childs + New Random NN's
#1 -> New population = Top performers + childs - N Worst Performers: Where N = number of childs
genetic_type=1
training_population = 100
#percentage of the population that reproduces
percentage_to_reproduce = 0.1
if(training_population*percentage_to_reproduce%2!=0 and training_population*percentage_to_reproduce>=2):
    raise Exception("training_population multipled by the percentage_to_reproduce must be an even number")
skip_menu = True
min_mutation=-0.01
max_mutation=0.01
default_mutation_rate=0.01
#Number of inputs for the NN
nn_nb_inputs=25
#Number of neurons in each hidden layers
nn_nb_hidden_layers = [25,50,100,200,100,50,25]
#Activation function
activation_function = "tahn"
fps = 10
max_steps = 100
