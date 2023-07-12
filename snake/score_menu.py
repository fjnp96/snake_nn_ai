#Menu
# import pygame package
import pygame
import menu_button
from main import fps

class ScoreMenu:
# creating a bool value which checks
# if game is running
    running = True
    fpsClock = pygame.time.Clock()
    objects = []
    def __init__(self,width,height,score):
        self.width = width
        self.height = height
        self.replay = False
        score = menu_button.MenuButton(width/3,height*0.15,width/3,height*0.2,"Score: "+str(score))
        score.color = "#FF0000"
        tryagain = menu_button.MenuButton(width/3,height*0.4,width/3,height*0.2,"Play Again",play_again)
        quit = menu_button.MenuButton(width/3,height*0.65,width/3,height*0.2,"Quit",quit_menu)
        self.objects.append(score)
        self.objects.append(tryagain)
        self.objects.append(quit)

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
        #pygame.quit()

    
def play_again(score_menu):
    score_menu.replay = True
    score_menu.running = False
def quit_menu(score_menu):
    score_menu.running = False
