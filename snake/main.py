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
import os
from genetic_algorithm import GeneticAlgorithm


def main(menu):
    if not os.path.exists("results"):
        os.mkdir("results")
    if(not config.skip_menu):
        mainMenu = menu.Menu(800,600)
        mainMenu.display()
    train_cycle()

#@profile
def train_cycle():
    layers_list = [[18,10],[20,12],[25,15]]
    for layers in layers_list:
        for act_fun in ["relu"]:
            alg = GeneticAlgorithm(2,act_fun,layers)
            alg.train(500)
            #YOU ARE TESTING THE GENETIC TYPES AFTER THE REFACTOR, MISSING: 1 and 2
            #train(initial_population,config.genetic_type,act_fun,layers)



if __name__ == "__main__":
    main(menu)
