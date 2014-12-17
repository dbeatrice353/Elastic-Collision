from world import World
from pygame.locals import *
import pygame
from sys import exit
from random import *
import math
import time

SCREEN_LENGTH = 580
SCREEN_WIDTH = 840
NUMBER_OF_BALLS = 10

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH), 0, 32)
    world = World(SCREEN_LENGTH,SCREEN_WIDTH)
    world.set_ball_list(NUMBER_OF_BALLS)
    clock = pygame.time.Clock()
    # Game loop:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        time_passed_seconds = clock.tick()/ 1000.0
        world.update(time_passed_seconds)
        world.render(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
