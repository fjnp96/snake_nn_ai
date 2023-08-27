#Menu
# import pygame package
import pygame
import menu_button
import config
from config import fps
from game import Game
from score_menu import ScoreMenu

class Menu:
# creating a bool value which checks
# if game is running
    running = True
    fpsClock = pygame.time.Clock()
    objects = []
    def __init__(self,width,height):
        self.width = width
        self.height = height
        start_button = menu_button.MenuButton(width*0.33,height*0.13,width*0.33,height*0.33,"Play",play)
        train_button = menu_button.MenuButton(width*0.33,height*0.57,width*0.33,height*0.33,"Train",train)
        self.objects.append(start_button)
        self.objects.append(train_button)

    def display(self):
        # initializing imported module
        pygame.init()
        #Display window with width/height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Menu')
        # Game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
            for i in self.objects:
                i.process(self)
            #updates the frames of the game
            pygame.display.flip()
            self.fpsClock.tick(fps)
        pygame.quit()

    
def play(menu):
    replay = True
    while replay:
        print("Repeat")
        game = Game(menu.width,menu.height,True)
        game.play()
        #SCORE MENU
        score_menu = ScoreMenu(menu.width,menu.height,game.score)
        score_menu.display()
        replay = score_menu.replay
        menu.screen.fill("#000000")

def train():
    pygame.quit()
    while(True):
        input("hello there type somehting:")


    
        
        
    




    
