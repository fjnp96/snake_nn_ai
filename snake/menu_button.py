#Menu Button
import pygame
pygame.font.init()
font = pygame.font.SysFont('Arial',40)
class MenuButton():
    def __init__(
        self,
        x,
        y,
        width,
        height,
        buttonText='Button',
        onclickFunction=None
        ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
            }
        self.buttonSurface = pygame.Surface((self.width,self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20,20,20))
        
    def process(self,menu):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if(self.onclickFunction!=None):
                    self.onclickFunction(menu)
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        menu.screen.blit(self.buttonSurface, self.buttonRect)

        
