#Game
import pygame
import random
import math
import numpy as np
import keyboard
from snake import Snake
from menu_button import MenuButton
from game_object import GameObject
from config import fps
from config import max_steps
from config import max_steps_reset_score
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

font = pygame.font.SysFont('Arial',40)

class Game:
    score = 0
    fpsClock = pygame.time.Clock()
    score_margin = 40
    points = 1
    #receives max width and height to know how to build
    #display: Boolean -> display this game?
    def __init__(self, width, height, display):
        #print("Game initializing...")
        self.object_size = width/40
        self.width = width
        self.height = height
        self.game_width = width-(self.score_margin*2)
        self.game_height = height-(self.score_margin*2)
        self.running = True
        self.display = display
        self.game_over = False

    #Game Cycle
    def play(self):
        self.setup_game()
        # Game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.key_pressed(event.key)
                    break
            if(self.display):
                self.display_game()
                #updates the frames of the game
                pygame.display.flip()
                self.fpsClock.tick(fps)
            self.game_cycle()

    #Cycle for NN to Play
    def play_nn(self, nn):
        self.setup_game()
        self.setup_nn_game()
        # Game loop
        while self.running:
            #Checks for max steps
            if(self.steps == max_steps):
                self.running = False
                if(max_steps_reset_score):
                    self.score=0
                break
            self.move_nn_snake(nn.predict(self.get_game_state()))
            if(keyboard.is_pressed("space")):
                self.display = False
            if(self.display):
                self.display_game()
                #updates the frames of the game
                pygame.display.flip()
                self.fpsClock.tick(fps)
            self.game_cycle()

    #Move NN snake based on the prediction list
    def move_nn_snake(self,predictions):
        move = np.argmax(predictions)
        #move can be either 0,1 or 2
        #0 -> rotate counter_clockwise
        #1 -> doesnt move
        #2 -> rotate clockwise
        direction = self.snake.direction
        if((move == 0 and direction=="east") or (move==2 and direction=="west")):
            self.snake.direction = "north"
        elif((move == 0 and direction=="south") or (move==2 and direction=="north")):
            self.snake.direction = "east"
        elif((move == 0 and direction=="west") or (move==2 and direction=="east")):
            self.snake.direction = "south"
        elif((move == 0 and direction=="north") or (move==2 and direction=="south")):
            self.snake.direction = "west"
        if(move!=1):
            self.turned=True
        if(self.prev_direction==self.snake.direction):
            self.count_same_direction +=1
        else:
            self.count_same_direction=0
        if(self.count_same_direction>8 and move!=0):
            self.score2 -=1
        else:
            self.score2+=2
        self.prev_direction=self.snake.direction
        #increment the steps taken
        self.steps = self.steps + 1

    def game_cycle(self):
        ate_food = self.ate_food()
        if(ate_food):
            self.score += 1
            self.generate_food()
            self.steps = 0
        if(not(self.game_over)):
            self.snake.move(ate_food)
        if(self.lose()):
            self.game_over = True
            self.running = False

    #returns true if it hit a wall or itself
    def lose(self):
        x = self.hit_wall() or self.hit_itself()
        if(x):
            self.hit_bool = True
        return x
    #sets a new method to call when the game is lost
    def set_on_lose_function(self, on_lose_function):
        self.on_lose_function = on_lose_function


    #returns true if it hit a wall
    def hit_wall(self):
        head = self.snake.body[0]
        max_width = self.game_width
        max_height = self.game_height
        return (head.x<0 or head.y<0 or head.x==max_width or head.y==max_height)

    def hit_itself(self):
        head = self.snake.body[0]
        for i in range(1,len(self.snake.body)):
            if(self.snake.body[i].x == head.x and self.snake.body[i].y == head.y):
                return True
        return False

    #return true if the snake Ate a Food
    def ate_food(self):
        head = self.snake.body[0]
        return head.x == self.food.x and head.y == self.food.y



    def display_game(self):
        #Display window with width/height
        self.screen.fill("#000000")
        self.game_screen.fill("#ffffff")
        self.score_screen.fill("#000000")
        self.food.draw(self.game_screen)
        self.draw_body()
        self.screen.blit(self.game_screen,(self.score_margin,self.score_margin))
        scoreSurf = font.render(str(self.score),True,"#ffffff")
        self.score_screen.blit(scoreSurf,(0,0))
        self.screen.blit(self.score_screen,(0,0))


    def setup_game(self):
        #Creates the Snake
        snake1 = [GameObject(60,40,self.object_size,self.object_size,"#e3dc45")]
        snake1.append(GameObject(40,40,self.object_size,self.object_size,"#d39d20"))
        snake1.append(GameObject(20,40,self.object_size,self.object_size,"#d39d20"))
        snake1.append(GameObject(0,40,self.object_size,self.object_size,"#d39d20"))
        self.snake = Snake(snake1)
        #Creates the Food
        food_x, food_y = self.random_food()
        self.food = GameObject(food_x,food_y,self.object_size,self.object_size,"#30ab1f")
        self.generate_food(True)
        if(food_x<0 or food_x>=self.game_width or food_y<0 or food_y>=self.game_height):
            raise Exception("Food position is not acceptable, x:",food_x," y:",food_y, " game_width:",self.game_width, " game_height:", self.game_height)

        if(self.display):
            pygame.display.set_caption('Snake Game')
            self.screen = pygame.display.set_mode((self.width, self.height))
            #Screen to display the game Screen
            self.game_screen =  pygame.Surface((self.game_width,self.game_height))
            #Screen to display the Score
            self.score_screen = pygame.Surface((self.score_margin*4,self.score_margin))
    def setup_nn_game(self):
        self.steps = 0
        self.turned=False
        self.hit_bool = False
        self.prev_direction = self.snake.direction
        self.count_same_direction = 0
        self.score2 = 0

    def draw_body(self):
        for body in self.snake.body:
            body.draw(self.game_screen)

    #Food Part
    def generate_food(self, same_line=False):
        food_x, food_y = self.random_food()
        head = self.snake.body[0]
        while(True):
            food_x,food_y = self.random_food()
            for i in self.snake.body:
                if(i.x==food_x and i.y==food_y):
                    continue
                elif((self.snake.direction=="east" or self.snake.direction=="west") and head.y == food_y):
                    continue
                elif((self.snake.direction=="north" or self.snake.direction=="south") and head.x == food_x):
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

    #Returns a list which will be the Input for the NN
    #This list will have 25 elements, which represent the 8 direction the snake looks and distance to food, itself, and the wall
    #plus the direction it is facing
    def get_game_state(self):
        game_state = []
        #MAGIC NUMBER TO BE CHANGED
        #It represents the squares width and height
        magic = 20
        #food
        food = (self.food.x/magic,self.food.y/magic)
        #Snake head
        head = (self.snake.body[0].x/magic,self.snake.body[0].y/magic)

        body = []
        for i in range(1,len(self.snake.body)):
            body.append((self.snake.body[i].x/magic,self.snake.body[i].y/magic))


        #distance to the food
        game_state.extend(get_food_distance(food,head))
        #distance to walls
        game_state.extend(get_distance_to_walls(head,self.game_width/magic,self.game_height/magic))
        #distance to itself
        game_state.extend(get_distance_to_itself(head,body))
        game_state.append(get_direction(self.snake.direction))
        return game_state



def get_direction(direction):
    directions = ["north","east","south","west"]
    return directions.index(direction)

# this function will return the 8 values for the food since only one can have a value
def get_food_distance(food, head):
    #[N,NE,E,SE,S,SW,W,NW]
    food_distance=[10000]*8
    #x axis
    if(solve(head,0,head[0],(food[1],food[0]))):
        d = math.dist(head,food)
        #Food is to the North
        if(head[1]>food[1]):
            food_distance[0] = d
        #Food is to the South
        else:
            food_distance[4] = d
    #y axis
    if(solve(head,0,head[1],food)):
        d = math.dist(head,food)
        #Food is to the East
        if(head[0]>food[0]):
            food_distance[2] = d
        #food is to West
        else:
            food_distance[6] = d
    #Diagonal
    #y=x
    if(solve(head,1,head[1]-head[0],food)):
        d = math.dist(head,food)
        #Food is to the NW
        if(head[0]>food[0]):
            food_distance[7] = d
        #Food is to the SE
        else:
            food_distance[3] = d
    #y=-x
    if(solve(head,-1,head[0]+head[1],food)):
        d = math.dist(head,food)
        #Food is to the SW
        if(head[0]>food[0]):
            food_distance[5] = d
        #Food is to the NE
        else:
            food_distance[1] = d
    return food_distance

def get_distance_to_walls(head,width,height):
    #[N,NE,E,SE,S,SW,W,NW]
    # Initialize wall distances
    wall_distances = [10000] * 8
    # Calculate the distance to the N wall
    wall_distances[0] = head[1]
     # Calculate the distance to the E wall
    wall_distances[2] = width - head[0]
    # Calculate the distance to the S wall
    wall_distances[4] = height - head[1]
    # Calculate the distance to the W wall
    wall_distances[6] = head[0]

    #Diagonal
    #Wall points
    up_wall = ((0,0),(width,0))
    right_wall = ((width,0),(width,height))
    down_wall = ((0,height),(width,height))
    left_wall = ((0,0),(0,height))

    #directions points
    ne_direction = (head,(head[0]+1,head[1]-1))
    se_direction = (head,(head[0]+1,head[1]+1))
    sw_direction = (head,(head[0]-1,head[1]+1))
    nw_direction = (head,(head[0]-1,head[1]-1))
    directions = (ne_direction,se_direction,sw_direction,nw_direction)
    for i, (a,b) in enumerate(directions):
        if(head[0]>head[1]):
            if(head[1]<height/2):
                walls = (up_wall,right_wall,left_wall,up_wall)
            else:
                walls = (right_wall,right_wall,down_wall,up_wall)
        else:
            if(head[1]>height/2):
                walls = (right_wall,down_wall,down_wall,left_wall)
            else:
                walls = (up_wall,down_wall,left_wall,left_wall)
        point = get_intersect(directions[i],walls[i])
        wall_distances[(i*2)+1] = math.dist(head,point)
    return wall_distances


def get_distance_to_itself(head,body):
    body.reverse()
    for i in body:
        #[N,NE,E,SE,S,SW,W,NW]
        distance=[10000]*8
        #x axis
        if(solve(head,0,head[0],(i[1],i[0]))):
            d = math.dist(head,i)
            #North
            if(head[1]>i[1]):
                distance[0] = d
            #South
            else:
                distance[4] = d
        #y axis
        if(solve(head,0,head[1],i)):
            d = math.dist(head,i)
            #East
            if(head[0]>i[0]):
                distance[2] = d
            #West
            else:
                distance[6] = d
        #Diagonal
        #y=x
        if(solve(head,1,head[1]-head[0],i)):
            d = math.dist(head,i)
            #NW
            if(head[0]>i[0]):
                distance[7] = d
            #SE
            else:
                distance[3] = d
        #y=-x
        if(solve(head,-1,head[0]+head[1],i)):
            d = math.dist(head,i)
            #SW
            if(head[0]>i[0]):
                distance[5] = d
            #NE
            else:
                distance[1] = d
    return distance




#given 2 points in a line and 2 points in another line
#return the point of intersection
def get_intersect(a, b):
    a1 = a[0]
    a2 = a[1]
    b1 = b[0]
    b2 = b[1]
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)
#y = mx+b
#checks if point is in function
def solve(head, m, b, point):
   return point[1] == (m * point[0]) + b

