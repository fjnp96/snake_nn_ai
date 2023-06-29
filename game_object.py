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
        self.buttonSurface.fill(self.color)
        screen.blit(self.buttonSurface, self.buttonRect)
