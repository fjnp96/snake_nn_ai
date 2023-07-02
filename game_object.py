#Game Objects
import pygame
class GameObject:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color="#ffffff"
        ):
        print("creating button")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.buttonSurface = pygame.Surface((self.width,self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self,screen):
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface.fill(self.color)
        screen.blit(self.buttonSurface, self.buttonRect)
    def set_x(self,new_x):
        self.x = new_x
    def set_y(self,new_y):
        self.y = new_y

    #Moves in X axis x amount of steps based on width
    def move_x(self, x):
        self.x =self.x + (x*self.width)
    #Moves in Y axis y amount of steps based on height
    def move_y(self, y):
        self.y = self.y + (y*self.height)






