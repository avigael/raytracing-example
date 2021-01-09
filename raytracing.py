'''2D Raytracing Example using Pygame'''
import sys
from math import pi, cos, sin
import pygame

# Constants
SIZE = (600, 600)
BORDERS = [[0, 0, SIZE[0], 0], [0, 0, 0, SIZE[1]],
           [0, SIZE[1], SIZE[0], SIZE[1]], [SIZE[0], 0, SIZE[0], SIZE[1]]]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Ray:
    '''create rays and see their intersections'''

    def __init__(self, x_1, y_1, x_2, y_2):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2

    def cast(self):
        '''see https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection'''
        # Checks Window Borders
        for border in BORDERS:
            x_3 = border[0]
            y_3 = border[1]
            x_4 = border[2]
            y_4 = border[3]
            P = (self.x_1 - self.x_2) * (y_3 - y_4) - \
                (self.y_1 - self.y_2) * (x_3 - x_4)
            if P != 0:
                t = ((self.x_1 - x_3) * (y_3 - y_4) -
                     (self.y_1 - y_3) * (x_3 - x_4))/P
                u = -((self.x_1 - self.x_2) * (self.y_1 - y_3) -
                      (self.y_1 - self.y_2) * (self.x_1 - x_3))/P
                if 0 <= t and u >= 0 and u <= 1:
                    point = ((self.x_2 - self.x_1) * t +
                             self.x_1, (y_4 - y_3) * u + y_3)
                    break

        # Checks Barriers
        for barrier in Barrier.collection:
            x_3 = barrier[0]
            y_3 = barrier[1]
            x_4 = barrier[2]
            y_4 = barrier[3]
            P = (self.x_1 - self.x_2) * (y_3 - y_4) - \
                (self.y_1 - self.y_2) * (x_3 - x_4)
            if P != 0:
                t = ((self.x_1 - x_3) * (y_3 - y_4) -
                     (self.y_1 - y_3) * (x_3 - x_4))/P
                u = -((self.x_1 - self.x_2) * (self.y_1 - y_3) -
                      (self.y_1 - self.y_2) * (self.x_1 - x_3))/P
                if 0 <= t and u >= 0 and u <= 1:
                    npoint = ((self.x_2 - self.x_1) * t +
                              self.x_1, (y_4 - y_3) * u + y_3)
                    if abs(npoint[0] - self.x_1) < abs(point[0] - self.x_1):
                        point = npoint
        # Draws Ray
        pygame.draw.aaline(screen, GREEN, (self.x_1, self.y_1), point)


class Radar:
    '''creates rays around a point'''

    def __init__(self, x, y, N):
        self.rays = []
        # N represents number of Rays
        for i in range(0, N):
            # Formula to create rays around a point
            ray = Ray(x, y, x + cos(i/N * 2 * pi), y + sin(i/N * 2 * pi))
            self.rays.append(ray)

    def radiate(self):
        '''emits rays'''
        for ray in self.rays:
            ray.cast()


class Barrier:
    '''create barriers for rays to intersect with'''
    collection = []

    def __init__(self, x_1, y_1, x_2, y_2):
        Barrier.collection.append([x_1, y_1, x_2, y_2])


def draw_barrier():
    '''draws Barriers'''
    for barrier in Barrier.collection:
        p_1 = (barrier[0], barrier[1])
        p_2 = (barrier[2], barrier[3])
        pygame.draw.aaline(screen, BLACK, p_1, p_2)


def create_map():
    '''initializes custom map'''
    width = SIZE[0]
    height = SIZE[1]
    Barrier(width/6, height, width/6, height/2)
    Barrier(width/3, height, width/3, height/1.5)
    Barrier(width/2, height/2, width/6, height/2)
    Barrier(width/2, height/1.5, width/3, height/1.5)
    Barrier(width/1.5, height/1.5, width/1.5, height/2)
    Barrier(width/1.2, height/2, width/1.5, height/2)
    Barrier(width/1.2, height/2, width/1.2, height/1.5)
    Barrier(width/1.5, height/1.5, width/1.2, height/1.5)
    Barrier(width/3, height/6, width/3, height/3)
    Barrier(width/3, height/6, width/2, height/3)
    Barrier(width/2, height/6, width/2, height/3)
    Barrier(width/2, height/6, width/1.5, height/3)
    Barrier(width/1.5, height/6, width/1.5, height/3)


# Initialize Screen
pygame.init()
pygame.display.set_caption("Raytracing Example")
screen = pygame.display.set_mode(SIZE)
create_map()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
    mouse = pygame.mouse.get_pos()
    radar = Radar(mouse[0], mouse[1], 25)
    screen.fill(WHITE)
    draw_barrier()
    radar.radiate()
