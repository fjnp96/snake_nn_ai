import time
import keyboard
from config import training_population
from config import percentage_to_crossover
from config import nr_processes
from game import Game
from neural_network import *
from statistics import mean
from itertools import repeat
from concurrent.futures import ProcessPoolExecutor
import plotly.graph_objs as go
import plotly.offline as offline

class GeneticAlgorithm:

    def __init__(self,genetic_type,act_func,hidden_layers):
        self.population = generate_population(0,training_population,act_func,hidden_layers)
        self.genetic_type = self.get_genetic_type(genetic_type)
        self.activation_function = act_func
        self.hidden_layers = hidden_layers
        self.display = False
        #Used for the IDs of the Snakes
        self.current_population = training_population
        #Mean of the top performers over the genarations
        self.top_performers_mean=[]

    def train(self,generations):
        start = time.time()
        running = True
        generation = 1
        #Mean of the top performers over the genarations
        while(running):
            self.genetic_type(generation)
            generation+=1
            #Stop cycle
            if(keyboard.is_pressed("space") or generation>generations):
                print("Next Iteration")
                break
            if(keyboard.is_pressed("q")):
                print("Quitting")
                quit()
                break
        end = time.time()
        print("Took ",end-start, " Seconds to run")
        print("top_performers_mean",self.top_performers_mean)
        print("Plotting")
        trace = go.Scatter(x=[i for i in range(1,generation+1,1)],y=self.top_performers_mean)
        offline.plot([trace], filename = "results/results"+str(self.genetic_type.__name__)+"-"+self.activation_function+str(self.hidden_layers)+".html")


    def genetic_algorithm1(self,generation):
        pop_score = self.play_population()
        sorted_score = get_sorted(pop_score)

        N = int(len(pop_score)*percentage_to_crossover)
        top_performers = sorted_score[:N]
        self.calculate_top_mean(pop_score,top_performers)
        print_top_scores(pop_score,top_performers,generation)

        new_population = {}
        #Crossover
        for i in range(0,len(top_performers),2):
            parent1 = self.population[top_performers[i]]
            parent2 = self.population[top_performers[i+1]]
            child1,child2 = parent1.random_crossover(parent2,self.current_population)
            new_population[top_performers[i]] = parent1
            new_population[top_performers[i+1]] = parent2
            new_population[self.current_population] = child1
            new_population[self.current_population+1] = child2
            self.current_population+=2

        #Mutation
        mutate_population(new_population)
        self.population=new_population
        self.fill_population()


    #similar to the first one but will remove the worst ones based how many child were created
    #new populaton = old population +childs - N worst ones where N = len(childs)
    def genetic_algorithm2(self,generation):
        pop_score = self.play_population()
        sorted_score = get_sorted(pop_score)

        N = int(len(pop_score)*percentage_to_crossover)
        top_performers = sorted_score[:N]

        self.calculate_top_mean(pop_score,top_performers)
        print_top_scores(pop_score,top_performers,generation)

        new_population = {}
        N=0
        #Crossover
        for i in range(0,len(top_performers),2):
            parent1 = self.population[top_performers[i]]
            parent2 = self.population[top_performers[i+1]]
            child1, child2 = parent1.random_crossover(parent2,self.current_population)
            new_population[self.current_population] = child1
            new_population[self.current_population+1] = child2
            self.current_population+=2
            N+=2
        mutate_population(new_population)
        #pop worst performers
        worst_performers = sorted_score[-N:]
        for worst_performer in worst_performers:
            self.population.pop(worst_performer)
        self.population.update(new_population)
        if(len(self.population)!=training_population):
            raise Exception("In genetic type 1 population size is different from training crossover_population, population_size",len(self.population))

    def genetic_algorithm3(self,generation):
        pop_score = self.play_population()
        sorted_score = get_sorted(pop_score)

        N = int(len(pop_score)*percentage_to_crossover)
        top_performers = sorted_score[:N]

        self.calculate_top_mean(pop_score,top_performers)
        print_top_scores(pop_score,top_performers,generation)

        worst_performers = sorted_score[N:len(pop_score)]

        new_population = {}
        for _ in range(round(len(worst_performers)/2)):
            parent1 = random.choice(top_performers)
            parent2 = random.choice(top_performers)
            while(parent1 == parent2):
                parent2 = random.choice(top_performers)
            child1, child2 = self.population[parent1].random_crossover(self.population[parent2],self.current_population)
            new_population[self.current_population] = child1
            new_population[self.current_population+1] = child2
            self.current_population+=2

        mutate_population(new_population)
        for key in top_performers:
            new_population[key] = self.population[key]

        #Case where it is an odd number
        if(len(new_population)+1==training_population):
            new_population.pop(self.current_population-1)
            self.current_population-=1

        if(len(new_population)!=config.training_population):
            raise Exception("In genetic type 2 population size is different from training crossover_population")

        self.population=new_population

    def play_population(self):
        pop_score = {}
        if(len(self.population)!=training_population):
            raise Exception("Error in population len : ",len(self.population))
        #Multiprocessing
        # start the process pool
        with ProcessPoolExecutor(config.nr_processes) as executor:
            # submit all tasks
            for score in executor.map(play_nn, self.population.values(), repeat(self.display)):
                pop_score[score[0]] = score[1]
        return pop_score

    def fill_population(self):
        start = self.current_population
        end = self.current_population + training_population - len(self.population)
        self.current_population = end
        self.population.update(generate_population(start,end,self.activation_function,self.hidden_layers))
        if(len(self.population)!=training_population):
            raise Exception("Population not filled until training_population, current_population:",len(self.population))

    def calculate_top_mean(self,pop_score,top_performers):
        scores = []
        for i in top_performers:
            scores.append(pop_score[i][1])
        self.top_performers_mean.append(mean(scores))

    def get_genetic_type(self,genetic_type_number):
        match genetic_type_number:
            case 0:
                return self.genetic_algorithm1
            case 1:
                return self.genetic_algorithm2
            case 2:
                return self.genetic_algorithm3
            case _:
                raise Exception("No or Wrong Genetic GeneticAlgorithm found, try 0,1 or 2")

def play_nn(nn,display):
    game = Game(800,600,display)
    game.play_nn(nn)
    return (nn.id,(game.score,fitness(game)))

def fitness(game):
    hit_score = 0
    if(game.hit_bool):
        hit_score = -250
    if(not game.turned):
        return 0
    return (game.score*5000)+game.score2+hit_score

def fitness1(game):
    steps =game.total_steps
    score = game.score
    return steps + (pow(2,steps)+(pow(score,2.1)*500)) - (pow(score,1.2)*pow((0.25*steps),1.3))

def get_sorted(pop_score):
    return [item[0] for item in sorted(pop_score.items(),key = lambda i: i[1][1],reverse = True)]


def print_top_scores(pop_score, top_performers, generation):
    print("//////////   Generation   /////////",generation)
    top_performer = top_performers[0]
    print("ID: ",top_performers[0])
    print("Food Ate",pop_score[top_performer][0])
    print("Score: ",pop_score[top_performer][1])
    if(pop_score[top_performer][1]==0):
        print(pop_score)

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

def mutate_population(population):
    for nn in population.values():
        nn.mutate()
