#! /usr/bin/env python

import os
import random
import pygame
import math
import time
import sys
import pyautogui as py
from random import seed
from random import randint
from math import atan2, degrees, pi




# Class for the orange dude
class Player(object):

    def __init__(self, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x, pos_y, 16, 16)
        self.collided_direction = -1  # remember if we have a collision 
        self.heading = 0  # where to go next
        self.average_velocity_x = 0  # remember how far travelled in x direction
        self.average_velocity_y = 0  # remember how far travelled in y direction
        self.mode = 0  # going towards food or searching in new direction
        self.angle = 0
        self.collide = False
        self.prev = 0
        self.prev_mov_x = 0
        self.prev_mov_y = 0

    def move(self, dx, dy):
        # self.collide = False
        # Move each axis separately. Note that this checks for collisions both times.
        # print('collided direction is ', self.collided_direction)
        # print(py.position())
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            #self.collided_direction = -1
            if self.rect.colliderect(wall.rect):
                self.collide = True
                print(" got collision in move_single_axis ")
                #print(dx)
                #print(dy)

                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    self.collided_direction = 1
                    print(' in 1')

                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    self.collided_direction = 2
                    print('in 2')

                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                    self.collided_direction = 3
                    print('in 3')

                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                    self.collided_direction = 4
                    print('in 4')


# Nice class to hold a wall rect
class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


class End(object):

    def __init__(self, pos):
        ends.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Bee Simulation!")
screen = pygame.display.set_mode((320, 240))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
ends = []  # list to hold endpoints
position_x = (int)(random.random() * 170) + 10
position_y = (int)(random.random() * 200) + 20
player = Player(position_x,position_y)  # Create the player
start_time = time.time()



# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W   W E W      W E W",
    "W   W   W      W   W",
    "W   W              W",
    "W   W              W",
    "W   WWWWWW    WWWWWW",
    "W        W    W    W",
    "W        W    W    W",
    "W        W    W    W",
    "W        W    W    W",
    "W        W    W    W",
    "W        W    W    W",
    "W                  W",
    "W                  W",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            End((x, y))
        x += 16
    y += 16
    x = 0

left_feeder_distance = math.sqrt((player.rect.x - ends[0].rect.x) ** 2 + (player.rect.y - ends[0].rect.y) ** 2)
right_feeder_distance = math.sqrt((player.rect.x - ends[1].rect.x) ** 2 + (player.rect.y - ends[1].rect.y) ** 2)
# Move the player based on clock time
if left_feeder_distance > right_feeder_distance:
    # Let the target be the left feeder
    targetR = right_feeder_distance
# print(targetR)
else:
    targetL = left_feeder_distance


def calcAngle():
    if left_feeder_distance > right_feeder_distance:
        # Let the target be the left feeder
        targetR = right_feeder_distance
        x1 = player.rect.x
        x2 = ends[1].rect.x
        y1 = player.rect.y
        y2 = ends[1].rect.y
        movex = x2 - x1
        movey = y2 - y1
        rads = atan2(-movey, movex)
        rads %= 2 * pi
        degs = degrees(rads)
        return degs
    # print(targetR)
    else:
        targetL = left_feeder_distance
        x1 = player.rect.x
        x2 = ends[0].rect.x
        y1 = player.rect.y
        y2 = ends[0].rect.y
        movex = x2 - x1
        movey = y2 - y1
        rads = atan2(-movey, movex)
        rads %= 2 * pi
        degs = degrees(rads)
        return degs

    # print(targetL)


def CalculateMinDist(): #make a method with an input variable for the end goal
    dist = [0, 0, 0, 0]
    if targetL > 0:
        moveDown()
        dist[0] = math.sqrt((player.rect.x - ends[0].rect.x) ** 2 + (player.rect.y - ends[0].rect.y) ** 2)
        moveUp()  # Gets player to original location

        moveLeft()
        dist[1] = math.sqrt((player.rect.x - ends[0].rect.x) ** 2 + (player.rect.y - ends[0].rect.y) ** 2)
        moveRight()  # Gets player to original location

        moveRight()
        dist[2] = math.sqrt((player.rect.x - ends[0].rect.x) ** 2 + (player.rect.y - ends[0].rect.y) ** 2)
        moveLeft()  # Gets player to original location

        moveUp()
        dist[3] = math.sqrt((player.rect.x - ends[0].rect.x) ** 2 + (player.rect.y - ends[0].rect.y) ** 2)
        moveDown()  # Gets player to original location
    elif targetR > 0:
        moveDown()
        dist[0] = math.sqrt((player.rect.x - ends[1].rect.x) ** 2 + (player.rect.y - ends[1].rect.y) ** 2)
        moveUp()  # Gets player to original location

        moveLeft()
        dist[1] = math.sqrt((player.rect.x - ends[1].rect.x) ** 2 + (player.rect.y - ends[1].rect.y) ** 2)
        moveRight()  # Gets player to original location

        moveRight()
        dist[2] = math.sqrt((player.rect.x - ends[1].rect.x) ** 2 + (player.rect.y - ends[1].rect.y) ** 2)
        moveLeft()  # Gets player to original location

        moveUp()
        dist[3] = math.sqrt((player.rect.x - ends[1].rect.x) ** 2 + (player.rect.y - ends[1].rect.y) ** 2)
        moveDown()  # Gets player to original location
    return dist

def SideGoal(x_target,y_target): #make a method with an input variable for the end goal
    dist = [0, 0, 0, 0]
    if targetL > 0:
        moveDown()
        dist[0] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveUp()  # Gets player to original location

        moveLeft()
        dist[1] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveRight()  # Gets player to original location

        moveRight()
        dist[2] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveLeft()  # Gets player to original location

        moveUp()
        dist[3] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveDown()  # Gets player to original location
    elif targetR > 0:
        moveDown()
        dist[0] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveUp()  # Gets player to original location

        moveLeft()
        dist[1] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveRight()  # Gets player to original location

        moveRight()
        dist[2] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveLeft()  # Gets player to original location

        moveUp()
        dist[3] = math.sqrt((player.rect.x - x_target) ** 2 + (player.rect.y - y_target) ** 2)
        moveDown()  # Gets player to original location
    return dist



def whereToMove():
    dist = CalculateMinDist()
    if dist.index(min(dist)) == 0:
        player.prev = 3
        return moveDown()
    elif dist.index(min(dist)) == 1:
        player.prev = 1
        return moveLeft()
    elif dist.index(min(dist)) == 2:
        player.prev = 2
        return moveRight()
    elif dist.index(min(dist)) == 3:
        player.prev = 4
        return moveUp()

def whereToMove_side(x,y):
    dist = SideGoal(x,y)
    if dist.index(min(dist)) == 0:
        return moveDown()
    elif dist.index(min(dist)) == 1:
        return moveLeft()
    elif dist.index(min(dist)) == 2:
        return moveRight()
    elif dist.index(min(dist)) == 3:
        return moveUp()
def moveAtAngle():
    x = int(math.sin(calcAngle()))
    y = int(math.cos(calcAngle()))
    rand1 = (int)(random.random() * 320) + 270
    x1 = int(math.sin(calcAngle()+rand1)*2) #end goal
    y1 = int(math.cos(calcAngle()+rand1)*2)
    #print((math.sin(calcAngle()+rand1)*2))
    #player.move(x1,y1)
    player.move(-2,0)
    #print("im here")

def moveLeft():
    player.move(-2, 0)


def moveRight():
    player.move(2, 0)


def moveUp():
    player.move(0, -2)


def moveDown():
    player.move(0, 2)


def randMove(rand):
    if rand == 1:
        moveLeft()
    elif rand == 2:
        moveRight()
    elif rand == 3:
        moveDown()
    elif rand == 4:
        moveUp()


def collided_dir():
    # collided = player.rect.collidelist(walls)
    # print ("collide list returned ", collided)
    return player.collided_direction

def randfunc(start, end):
    return (int)(random.random() * end) + start
x_pos = []
y_pos = []
running = True
while running:
    temp = randfunc(1,5)
    clock.tick(60)
    time.sleep(0.0005)
    print(collided_dir())
    # print(rand)
    x_pos.append(player.rect.x)
    y_pos.append(player.rect.y)
    player.prev_mov_x = player.rect.x
    player.prev_mov_y = player.rect.y
    #x_pos = set(x_pos)
    #y_pos = set(y_pos)
    if(collided_dir() == 1):
        moveLeft()
        player.prev = 1
        player.collided_direction = -1
    elif(collided_dir() == 2):
        moveRight()
        player.prev = 2
        player.collided_direction = -1
    elif(collided_dir == 3):
        moveDown()
        player.prev = 3
        player.collided_direction = -1
    elif(collided_dir == 4):
        moveUp()
        player.prev = 4
        player.collided_direction = -1
    else:
        whereToMove()
        if(collided_dir() == player.prev):#this section prevents the bee from getting stuck
            if((player.prev == 1) or (player.prev == 2)):
                randMove(randfunc(3,5))
            else:
                randMove(randfunc(1,3))
        if((player.prev_mov_x == player.rect.x) and (player.prev_mov_y == player.rect.y)):
            for x in range(100):
                randMove(randfunc(1,5))
        #if((len(x_pos)>=2 and len(y_pos)>=2):
           
           
            
            
        
                
                
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
        
    
    
    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for end in ends:
        pygame.draw.rect(screen, (255, 0, 0), end.rect)
        if player.rect.colliderect(end.rect):
            raise SystemExit
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()
