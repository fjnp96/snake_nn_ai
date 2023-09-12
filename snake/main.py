import menu
import config
import io
import time
import keyboard
import copy
from concurrent.futures import ProcessPoolExecutor
from game import Game
from neural_network import *
from memory_profiler import profile
from statistics import mean
from matplotlib import pyplot as plt
from itertools import repeat
import plotly.graph_objs as go
import plotly.offline as offline


def main(menu):
    if(not config.skip_menu):
        mainMenu = menu.Menu(800,600)
        mainMenu.display()
    train_cycle()
#@profile
def train_cycle():
    layers_list = [[18,10],[20,12],[25,15]]
    for layers in layers_list:
        for act_fun in ["relu"]:
            initial_population = generate_population(0,config.training_population,act_fun,layers)
            train(initial_population,config.genetic_type,act_fun,layers)

def train(initial_population,genetic_type,activation_function,hidden_layers):
    start = time.time()
    #number of id's in population
    current_population=config.training_population
    population = copy.deepcopy(initial_population)
    #print("CONFIGGENETICTYPE: ",config.genetic_type)
    #print("Config activation function: ",config.activation_function)
    running = True
    generation = 1
    #variable to start showing the NN's
    display = False
    #Mean of the top performers over the genarations
    top_performers_mean = []
    while(running):
        population, current_population = genetic_algorithm(genetic_type,population,top_performers_mean,current_population, generation, hidden_layers)
        generation+=1
        #Stop cycle
        if(keyboard.is_pressed("space") or generation>500):
            break
        if(keyboard.is_pressed("q")):
            quit()
            break
    end = time.time()
    print("Took ",end-start, " Seconds to run")
    print("top_performers_mean",top_performers_mean)
    print("Plotting")
    trace = go.Scatter(x=[i for i in range(1,generation+1,1)],y=top_performers_mean)
    offline.plot([trace], filename = "results"+str(genetic_type)+"-"+activation_function+str(hidden_layers)+".html")

def genetic_algorithm(genetic_type,population,top_performers_mean,current_population, generation, hidden_layers):
    if(genetic_type==0):
        #pop_score = {}
        # {id:(score,score+steps)}
        pop_score = play_population(population)
        #List of NN id's sorted by score
        top_performers = pick_top(pop_score)
        calculate_top_mean(top_performers_mean,pop_score,top_performers)
        print_top_scores(pop_score, top_performers, generation)
        population, current_population = crossover_population(population,top_performers,current_population)
        mutate_population(population)
        current_population = fill_population(population,current_population,hidden_layers)

    if(genetic_type==1):
        #Play population and get Scores
        pop_score = play_population(population)
        #SOrt the Scores
        sorted_score = get_sorted(pop_score)
        N = int(len(pop_score)*config.percentage_to_reproduce)
        top_performers = sorted_score[:N]
        calculate_top_mean(top_performers_mean,pop_score,top_performers)
        print_top_scores(pop_score,top_performers,generation)
        current_population = crossover_population2(population,sorted_score,top_performers,current_population)
        mutate_population(population)
    if(genetic_type==2):
        #Play population and get Scores
        pop_score = play_population(population)
        #SOrt the Scores
        sorted_score = get_sorted(pop_score)
        N = int(len(pop_score)*config.percentage_to_reproduce)
        top_performers = sorted_score[:N]

        calculate_top_mean(top_performers_mean,pop_score,top_performers)
        print_top_scores(pop_score,top_performers,generation)

        worst_performers = sorted_score[N:len(pop_score)]
        old_population = copy.deepcopy(population)
        population , current_population = crossover_population3(population,top_performers,worst_performers,current_population)
        #mutate_population(population)
    return population, current_population


def generate_population(start,end,activation_function, hidden_layers):
    population = {}
    layers = hidden_layers
    for i in range(start,end,1):
        nn = Network(i)
        #add first layer based on number of inputs
        nn.add(FCLayer(config.nn_nb_inputs,layers[0]))
        nn.add(ActivationLayer(get_activation_function(activation_function)))
        for j in range(1,len(layers)):
            nn.add(FCLayer(layers[j-1],layers[j]))
            nn.add(ActivationLayer(get_activation_function(activation_function)))
        #add Output Layer
        nn.add(FCLayer(layers[len(layers)-1],3))
        nn.add(ActivationLayer(sig))
        population[nn.id]=nn
    return population

def play_population(population, display=False):
    pop_score = {}
    if(len(population)!=config.training_population):
        raise Exception("Error in population len : ",len(population))
    #Multiprocessing
    # start the process pool
    start1 = time.time()
    with ProcessPoolExecutor(8) as executor:
        # submit all tasks
        for score in executor.map(play_nn, population.values(), repeat(display)):
            pop_score[score[0]] = score[1]
    return pop_score

def play_nn(nn,display):
    game = Game(800,600,display)
    game.play_nn(nn)
    return (nn.id,(game.score,get_score(game)))


def pick_top(pop_score):
    N = int(len(pop_score)*config.percentage_to_reproduce)
    #List of NN id's sorted by score
    return [item[0] for item in sorted(pop_score.items(),key = lambda i: i[1][1],reverse = True)[:N]]

def get_sorted(pop_score):
    return [item[0] for item in sorted(pop_score.items(),key = lambda i: i[1][1],reverse = True)]

def crossover_population(population, top_performers,current_population):
    #In here we are creating a new population with the parents and childs
    new_population = {}
    #Crossover
    for i in range(0,len(top_performers),2):
        parent1 = population[top_performers[i]]
        parent2 = population[top_performers[i+1]]
        child = parent1.random_crossover(parent2,current_population)
        new_population[top_performers[i]] = parent1
        new_population[top_performers[i+1]] = parent2
        new_population[current_population] = child
        current_population=current_population+1
    return new_population, current_population

#similar to the other one but will remove the worst ones based how many child were created
#new populaton = old population +childs - N worst ones where N = len(childs)
def crossover_population2(population,sorted_score,top_performers,current_population):
    N = int(len(population)*config.percentage_to_reproduce)
    top_performers = sorted_score[:N]
    N=0
    #Crossover
    for i in range(0,len(top_performers),2):
        parent1 = population[top_performers[i]]
        parent2 = population[top_performers[i+1]]
        child = parent1.random_crossover(parent2,current_population)
        #population[top_performers[i]] = parent1
        #population[top_performers[i+1]] = parent2
        population[current_population] = child
        current_population=current_population+1
        N+=1
    #pop worst performers
    worst_performers = sorted_score[-N:]
    for worst_performer in worst_performers:
        population.pop(worst_performer)
    if(len(population)!=config.training_population):
        raise Exception("In crossover_population_2 population size is different from training crossover_population")
    return current_population

def crossover_population3(population,top_performers,worst_performers,current_population):
    new_population = {}
    for i in worst_performers:
        parent1 = random.choice(top_performers)
        parent2 = random.choice(top_performers)
        while(parent1 == parent2):
            parent2 = random.choice(top_performers)
        if(current_population in population.keys()):
            raise Exception("Error adding new child because key/id already in population")
        new_population[current_population] = population[parent1].random_crossover(population[parent2],current_population)
        current_population=current_population+1
    mutate_population(new_population)
    for key in top_performers:
        new_population[key] = population[key]
    if(len(population)!=config.training_population):
        raise Exception("In crossover_population_2 population size is different from training crossover_population")
    return new_population, current_population


def mutate_population(population):
    for nn in population.values():
        nn.mutate()

def fill_population(population, current_population, activation_function,hidden_layers):
    start = current_population
    end = current_population + config.training_population - len(population)
    current_population = current_population + config.training_population - len(population)
    population.update(generate_population(start,end,activation_function,hidden_layers))
    if(len(population)!=config.training_population):
        raise Exception("Population not filled until training_population, current_population:",len(population))
    return current_population

def print_top_scores(pop_score, top_performers, generation):
    print("//////////   Generation   /////////",generation)
    top_performer = top_performers[0]
    print("ID: ",top_performers[0])
    print("Food Ate",pop_score[top_performer][0])
    print("Score: ",pop_score[top_performer][1])
    if(pop_score[top_performer][1]==0):
        print(pop_score)

def calculate_top_mean(top_performers_mean,pop_score,top_performers):
    scores = []
    for i in top_performers:
        scores.append(pop_score[i][1])
    top_performers_mean.append(mean(scores))

def equal(x):
    return x

def get_score(game):
    hit_score = 0
    if(game.hit_bool):
        hit_score = -250
    if(not game.turned):
        return 0
    return (game.score*5000)+game.score2+hit_score

if __name__ == "__main__":
    main(menu)
