#Menu
# import pygame package
import pygame
import menu_button
from main import fps
from game import Game

class Menu:
# creating a bool value which checks
# if game is running
    running = True
    fpsClock = pygame.time.Clock()
    objects = []
    def __init__(self,width,height):
        self.width = width
        self.height = height
        start_button = menu_button.MenuButton(width/3,height/3,width/3,height/3,"Play",play)
        self.objects.append(start_button)

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
            for i in self.objects:
                i.process(self)
            #updates the frames of the game
            pygame.display.flip()
            self.fpsClock.tick(fps)
        pygame.quit()

    
def play(menu):
    replay = True
    while replay:
        game = Game(menu.width,menu.height,True)

    
        
        
    




    
