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
    nn = Network()
    nn.add(FCLayer(2,3))
    nn.add(ActivationLayer(tanh))
    nn.add(FCLayer(3,1))
    nn.add(ActivationLayer(tanh))
    nn.print()
    nn.mutate()
    nn.print()

if __name__ == "__main__":
    main(menu)

