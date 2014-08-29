#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Flappy Bird Clone by Mischka

# background image by Alucard (http://opengameart.org/users/alucard)
# plane image by kenney (http://opengameart.org/users/kenney)


''' Todo:
* add plane animation
* scroll background image endless
* obstacle disappear smoother
* add splash screen
* add high score
* add music
* rewrite code using the pygame methods (for collision)
* clean up code
'''

import sys

try: 
    import pygame
except:
    print "pygame not found, pls install pygame"
    sys.exit()


import random


### initialize pygame, start a frame, set pygame basic parameters
pygame.init()


# Colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
DARK_GREY = ( 31, 31, 40)


size = (700, 500)
screen = pygame.display.set_mode(size)
background_image = pygame.transform.scale(pygame.image.load("media/city_background_night.png").convert(), [8000, 500])
plane = pygame.transform.scale(pygame.image.load("media/planeBlue1.png").convert_alpha(), [70, 50])



pygame.display.set_caption("Flappy foo")

done = False
clock = pygame.time.Clock()

my_font = pygame.font.SysFont("monospace", 20, True)


# Variables:
time = 0
points = 0
coll = False
start = False

# initial position and size of the rectangle / plane
rect_x = size[0] / 2
rect_y = 40
rect_velocity = 0
rect_size_x = 70
rect_size_y = 50

# initial position of the background image (x pos)
back_pos_x = 0

# init set of obstacles
obstacles = set()

# set timer for pushing obstacles on the screen
pygame.time.set_timer(1, 2000)

# obstacle class

class obstacle:
    ''' class for the obstacles '''
    
    def __init__(self, color, pos_and_size, up):
        
        self.color = DARK_GREY
        self.pos_and_size = pos_and_size
        self.up = up
        self.velocity = 2
        self.passed = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.pos_and_size, 0)

    def update(self):
        ''' updates the position of the obstacle (it is moving from right
            to left); then checks if it has passed the middle of the screen
            (read: the bird passed the obstacle) - add one point '''
        global points
        self.pos_and_size[0] -= self.velocity
        if self.pos_and_size[0] < size[0] / 2 and not self.passed and not coll:
            points += .5
            self.passed = True

    def get_height(self):
        return self.pos_and_size[3]
    
    def get_width(self):
        return self.pos_and_size[0] + self.pos_and_size[2]
    
    def get_pos(self):
        return (self.pos_and_size[0], self.pos_and_size[1])

    def up(self):
        return self.up

    def stop():
        self.velocity = 0
        return True


    

def create_obstacles():
    upper_height = random.randrange(size[1] / 3, size[1] / 3  * 2) 

    obstacles.add(obstacle(BLACK, [size[0], 0, 80, upper_height], True))
    obstacles.add(obstacle(BLACK, [size[0], upper_height + 200, 80, size[1]], False)) # 200 für yunus eingestellt

def discard_obstacles():
    for obstacle in set(obstacles):
        if obstacle.get_pos()[0] + obstacle.get_width() < -60:
            obstacles.discard(obstacle)

def collision():
    collision = True
    for obstacle in obstacles:
        if obstacle.up:
            if (rect_y <= obstacle.get_height() and
                rect_x + rect_size_x >= obstacle.get_pos()[0] and
                rect_x <= obstacle.get_width()):
                collision = False
                return True
        elif not obstacle.up:
            if (rect_y + rect_size_y >= obstacle.get_pos()[1] and
                rect_x + rect_size_x >= obstacle.get_pos()[0] and
                rect_x <= obstacle.get_width()):
                collision = False
                return True
        
            
            
    return False
          
# Main loop
while not done:
    
    # event:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == 1:
            create_obstacles()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not coll:
                time = 0
                rect_velocity = -3
            if event.key == pygame.K_UP and coll:
                start = False
            elif event.key == pygame.K_UP and not start:
                start = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and not coll:
                rect_velocity = 0
        
              
            
                

    # clear screen, set it to white:
    # screen.fill(WHITE)

    
    # game start - reset globals
    
    if start == False:
        obstacles = set()
        points = 0
        coll = False
        rect_y = 40
        
    # some logic

    if collision():
        coll = True

    # fall down if not flapping
    if start == True and not (rect_y > size[1]):
        rect_velocity += 0.1
        rect_y += rect_velocity




    
    # draw things on the screen:
    

    # background image
    screen.blit(background_image, [back_pos_x, 0])
    if back_pos_x >= -7300:
        back_pos_x -= 1
    else:
        back_pos_x = 0

    # draw plane:
    #pygame.draw.rect(screen, WHITE, [rect_x,rect_y,rect_size_x,rect_size_y], 0)
    screen.blit(plane, [rect_x, rect_y])
    
    # obstacles:
    for item in obstacles:
        item.draw()
        item.update()

    # on screen text:
    points_txt = my_font.render("Points: " + str(int(points)),1, BLACK)
    game_over = my_font.render("Game Over * Press UP to restart", 1, BLACK)
    screen.blit(points_txt, (10, 10))
    if coll == True:
        screen.blit(game_over, (size[0] / 2 - 200, size[1] / 2 ))
        
    
    # discard if not needed anymore
    discard_obstacles()
    
    # update screen
    pygame.display.flip()






    clock.tick(60)

# shutdown pygame
pygame.quit()



    
