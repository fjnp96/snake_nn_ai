import pygame

class Snake:
    clockwise = {"north":"east","east":"south","south":"west","west":"north"}
    counterclockwise = {"north":"west","west":"south","south":"east","east":"north"}

    #body=list(GameObject)
    def __init__(self, body):
        print("Snake Created")
        self.body = body
        self.direction = "east"

    def move(self):
        #move rest of the body
        for i in range(len(self.body)-1,0,-1):
            self.body[i].set_x(self.body[i-1].x)
            self.body[i].set_y(self.body[i-1].y)
        #move snake's head
        if(self.direction =="north"):
            self.body[0].move_y(-1)
        elif(self.direction=="south"):
            self.body[0].move_y(1)
        elif(self.direction=="west"):
            self.body[0].move_x(-1)
        elif(self.direction=="east"):
            self.body[0].move_x(1)

    #rotate in direction clockwise=0 counterclockwise=1
    def rotate(self, direction):
        if(direction==0):
            print("rotate")
            self.direction = self.clockwise[self.direction]
        elif(direction==1):

            self.direction = self.counterclockwise[self.direction]



