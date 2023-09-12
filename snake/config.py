#Config file
#Genetic Type
#0 -> New population = Top performers + childs + New Random NN's
#1 -> New population = Top performers + childs - N Worst Performers: Where N = number of childs
#2 -> New population = Top performers + mutated(childs): Where N childs = Total population - Top performers. Picks random parents to mutate
genetic_type=2
training_population = 500
#percentage of the population that reproduces
percentage_to_reproduce = 0.1
if(training_population*percentage_to_reproduce%2!=0 and training_population*percentage_to_reproduce>=2):
    raise Exception("training_population multipled by the percentage_to_reproduce must be an even number")
skip_menu = True
min_mutation=-0.1 #beetween -0.5 and 0.5
max_mutation=0.1
#set random_mutation to True to mutate to a random number and ignore the two above values
random_mutation=False
default_mutation_rate=0.05
#Number of inputs for the NN
nn_nb_inputs=25
#Number of neurons in each hidden layers
nn_nb_hidden_layers = [16]
fps = 10

max_steps = 200
#Reset score when max_steps
max_steps_reset_score=True

#Activation function
activation_functions = ["tanh", "relu"]
