from vector import Vector2
from pygame.locals import *
from sys import exit
import pygame
import math


class Mouse:
    def __init__(self):
        self.px = 0
        self.py = 0
        self.vx = 0
        self.vy = 0
        self.radius = 40
        self.mass = math.pi*self.radius
        self.color = (100,200,100)

    def update(self,time_passed):
        px_temp = self.px
        py_temp = self.py
        self.px, self.py = pygame.mouse.get_pos()
        if time_passed != 0:
            self.vx = (self.px - px_temp)/time_passed
            self.vy = (self.py - py_temp)/time_passed

    def render(self,screen):
        pygame.draw.circle(screen,self.color,(self.px,self.py),self.radius)

