#Game
import pygame
import random
from main import fps

class Game:
    snake = []
    score = 0
    fpsClock = pygame.time.Clock()
    #receives max width and height to know how to build
    def __init__(self, screen, width, height):
        print("Game initializing...")
        self.width = width
        self.height = height
        self.running = True
        self.display(screen)

    def display(self,screen):
        self.setup_game()
        #Display window with width/height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        # Game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.food.draw(self.screen)
            #updates the frames of the game
            pygame.display.flip()
            self.fpsClock.tick(fps)
        pygame.quit(self.screen)

    def setup_game(self):
        from game_object import GameObject
        food_x = random.randint(0,self.width)
        food_y = random.randint(0,self.height)
        self.food = GameObject(food_x,food_y,20,20,"#000333")



