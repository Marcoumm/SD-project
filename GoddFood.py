import pygame, random, sys
from pygame.locals import *

# https://www.w3schools.com/python/python_classes.asp

class Food:
    
    def __init__(self, windowWidth, windowHeight, color, left, top, size):
        self.color = color
        self.rect = pygame.Rect(random.randint(0, windowWidth - size), 0 - size, size, size)
        


    def myfunc(self):
        print("Hello my name is " + self.name)

class BadFood(Food):
    
    def __init__(self, color):
        super().__init__(color)
        self.name = "Bad Food"