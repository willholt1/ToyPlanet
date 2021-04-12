import Food
import Creature
import random
import math
import numpy as np
import pygame

class Herbivore(Creature.Creature):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        
    def getData(self):
        pass