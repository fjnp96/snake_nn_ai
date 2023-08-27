import menu
import config
from game import Game
from neural_network import *

def main(menu):
    if(not config.skip_menu):
        mainMenu = menu.Menu(800,600)
        mainMenu.display()
    train()

def train():
    #number of id's in population
    current_population=config.training_population
    population = generate_population(0,config.training_population)
    running = True
    generation = 1
    #variable to start showing the NN's
    display = False
    while(running):
        #pop_score = {}
        # {id:(score,score+steps)}
        pop_score = play_population(population)
        #List of NN id's sorted by score
        top_performers = pick_top(pop_score)
        print_top_scores(pop_score, top_performers, generation)
        population, current_population = crossover_population(population,top_performers,current_population)
        mutate_population(population)
        current_population = fill_population(population,current_population)
        generation+=1
        if(generation>=100):
            break


def generate_population(start,end):
    population = {}
    layers = config.nn_nb_hidden_layers
    activation_function = get_activation_function()
    for i in range(start,end,1):
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
        population[nn.id]=nn
    return population

def play_population(population, display=False):
    pop_score = {}
    if(len(population)!=config.training_population):
        raise Exception("Error in population len : ",len(population))
    for nn in population.values():
        game = Game(800,600,display)
        game.play_nn(nn)
        #print("Id:",nn.id," Score:",game.score)
        pop_score[nn.id] = (game.score,get_score(game))
    return pop_score

def pick_top(pop_score):
    N = int(len(pop_score)*config.percentage_to_reproduce)
    #List of NN id's sorted by score
    return [item[0] for item in sorted(pop_score.items(),key = lambda i: i[1][1],reverse = True)[:N]]

def crossover_population(population, top_performers,current_population):
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

def mutate_population(population):
    for nn in population.values():
        nn.mutate()

def fill_population(population, current_population):
    start = current_population
    end = current_population + config.training_population - len(population)
    current_population = current_population + config.training_population - len(population)
    population.update(generate_population(start,end))
    if(len(population)!=config.training_population):
        raise Exception("Population not filled until training_population, current_population:",len(population))
    return current_population

def print_top_scores(pop_score, top_performers, generation):
    print("//////////   Generation   /////////",generation)
    top_performer = top_performers[0]
    print("ID: ",top_performers[0])
    print("Food Ate",pop_score[top_performer][0])
    print("Score: ",pop_score[top_performer][1])

def equal(x):
    return x

def get_score(game):
    return (game.score*100)+game.steps

if __name__ == "__main__":
    main(menu)

