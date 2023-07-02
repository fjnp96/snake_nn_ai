#Game
import pygame
import random
from main import fps
from snake import Snake
from menu_button import MenuButton
from game_object import GameObject

font = pygame.font.SysFont('Arial',40)

class Game:
    score = 500
    fpsClock = pygame.time.Clock()
    score_margin = 40
    #receives max width and height to know how to build
    #display: Boolean -> display this game?
    def __init__(self, width, height, display):
        print("Game initializing...")
        self.object_size = width/40
        self.width = width
        self.height = height
        self.game_width = width-(self.score_margin*2)
        self.game_height = height-(self.score_margin*2)
        self.running = True
        self.display = display
        self.play()

    #Game Cycle
    def play(self):
        self.setup_game()
        # Game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.key_pressed(event.key)
                    self.generate_food()
                    break
            if(self.display):
                self.display_game()
            self.snake.move()
            #updates the frames of the game
            pygame.display.flip()
            self.fpsClock.tick(fps)
        pygame.quit()

    def display_game(self):
        #Display window with width/height
        self.screen.fill("#000000")
        self.game_screen.fill("#ffffff")
        self.food.draw(self.game_screen)
        self.draw_body()
        self.screen.blit(self.game_screen,(self.score_margin,self.score_margin))
        scoreSurf = font.render(str(self.score),True,"#ffffff")
        self.score_screen.blit(scoreSurf,(0,0))
        self.screen.blit(self.score_screen,(0,0))


    def setup_game(self):
        #Creates the Food
        food_x, food_y = self.random_food()
        self.food = GameObject(food_x,food_y,self.object_size,self.object_size,"#30ab1f")
        #Creates the Snake
        snake1 = [GameObject(40,20,self.object_size,self.object_size,"#e3dc45"),GameObject(20,20,self.object_size,self.object_size,"#d39d20")]
        self.snake = Snake(snake1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        #Screen to display the game Screen
        self.game_screen =  pygame.Surface((self.game_width,self.game_height))
        #Screen to display the Score
        self.score_screen = pygame.Surface((self.score_margin*4,self.score_margin))
        pygame.display.set_caption('Snake Game')

    def draw_body(self):
        for body in self.snake.body:
            body.draw(self.game_screen)

    #Food Part
    def generate_food(self):
        food_x, food_y = self.random_food()
        while(True):
            for i in self.snake.body:
                if(i.x==food_x and i.y==food_y):
                    food_x,food_y = self.random_food()
                    continue
            break
        self.food.set_x(food_x)
        self.food.set_y(food_y)

    def random_food(self):
        x= random.randrange(0,self.game_width-self.object_size,self.object_size)
        y = random.randrange(0,self.game_height-self.object_size,self.object_size)
        return x,y

    def key_pressed(self, key):
        if(key == pygame.K_UP):
            if(self.snake.direction == "east" or self.snake.direction == "west"):
                self.snake.direction = "north"
                print("north")
        elif(key == pygame.K_RIGHT):
            if(self.snake.direction =="north" or self.snake.direction == "south"):
                self.snake.direction = "east"
                print("east")
        elif(key == pygame.K_DOWN):
            if(self.snake.direction == "east" or self.snake.direction == "west"):
                self.snake.direction = "south"
                print("south")
        elif(key == pygame.K_LEFT):
            if(self.snake.direction == "north" or self.snake.direction =="south"):
                self.snake.direction = "west"
                print("west")



