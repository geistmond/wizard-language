# Ultimately this goes into the Wizard Language project to model interactions.

import pygame
from pygame.locals import *
import pymunk
import pylab

import random
import io
import base64

# https://www.pygame.org/wiki/MatplotlibPygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg

fig = pylab.figure(figsize=[8,8], dpi=100,)
fig.patch.set_alpha(0.1)
ax = fig.gca()

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()

pygame.init()

display = pygame.display.set_mode((800, 800))
screen = pygame.display.get_surface()
size = canvas.get_width_height()
surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (0,0))
pygame.display.flip()
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 90

population = 300

recovery_time = 300 # depends on framerate FPS

class Ball():
    def __init__(self, x, y, r=10):
        self.x = x
        self.y = y
        self.r = r
        self.body = pymunk.Body()
        self.body.position = x, y
        self.mass = 100
        self.shape = pymunk.Circle(self.body, self.r)
        self.shape.density = 1.0
        self.shape.elasticity = 1.0
        self.shape.friction = 1.0
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.r)
        self.infected_time = 0
        self.infected = False
        self.recovered = False
        if self.infected == False:
            self.body.velocity = random.uniform(-100, 100), random.uniform(-100,100)
        elif self.infected == True:
            self.body.velocity = random.uniform(-25, 25), random.uniform(-25, 25) # quarter speed while infected
        space.add(self.body, self.shape)
        
    def pass_time(self):
        if self.infected:
            self.infected_time += 1
        if self.infected_time >= recovery_time:
            self.recover()
            self.shape.collision_type = population+2
        
    def draw(self):
        x, y = self.body.position
        if self.infected:
            pygame.draw.circle(display, (255,0,0), self.body.position, self.r)
        elif self.recovered:
            pygame.draw.circle(display, (0,0,255), self.body.position, self.r)
        else:
            pygame.draw.circle(display, (255,255,255), self.body.position, self.r)
            
    def infect(self, space=0, arbiter=0, data=0):
        if random.randint(0,100) > 50: # set to 50% chance, add more nuance later
            self.infected = True
        self.shape.collision_type = population + 1
        
    def recover(self, space=0, arbiter=0, data=0):
        self.infected = False
        self.recovered = True

class Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)


infected_count = []
def game():
    balls = [Ball(random.randint(0,800), random.randint(0,800), 10) for i in range(300)]
    
    for i in range(1, population+1):
        balls[i-1].shape.collision_type = i
        handler = space.add_collision_handler(i, population+1)
        handler.separate = balls[i-1].infect
        
    random.choice(balls).infect() # choose random agent to infect
    
    walls = [Wall((0, 0), (0, 800)), 
             Wall((0, 0), (800, 0)),
             Wall((0, 800), (800, 800)),
             Wall((800, 0), (800, 800))]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((0,0,0))
        infected_count_thisframe = 0
        recovered_count_thisframe = 0
        for ball in balls:
            ball.draw()
            ball.pass_time()
            if ball.infected:
                infected_count_thisframe += 1
            if ball.recovered:
                recovered_count_thisframe += 1
        infected_count.append(infected_count_thisframe)
        ax.plot(range(0, len(infected_count), 1), infected_count)
        
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()

#plt.plot(range(0, len(infected_count), 1), infected_count)

pygame.quit()