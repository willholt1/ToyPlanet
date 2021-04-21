import Food
import Creature
import random
import math
import numpy as np
import pygame
import constants

class Predator(Creature.Creature):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = 1

    #Override
    def update(self, foodList, action):
        if (self.sleepCounter < 500):
            self.sleepCounter += 1
            if (self.sleepCounter == 500):
                    self.originalImage = pygame.image.load('sprites/creature_red.png').convert_alpha()
                    self.image = self.originalImage
        else:
            if (constants.HTRAINPREDATORMOVE == True):
                if (self.energy > 0):
                    #perform action determined by the NN
                    if (action == constants.MOVE):
                        Creature.Creature.move(self)
                    elif (action == constants.TURNLEFT):
                        Creature.Creature.turnLeft(self)
                        Creature.Creature.move(self)
                    elif (action == constants.TURNRIGHT):
                        Creature.Creature.turnRight(self)
                        Creature.Creature.move(self)

                    self.look(foodList)
                    foodList = self.checkEat(foodList)
                    self.energy -= 1
                else:
                    if (self.foodEaten == 0):
                        self.fitness -= 10
                    self.rect.centerx = 0
                    self.rect.centery = 0
                    self.alive = False
            else:
                foodList = self.checkEat(foodList)
        return foodList

    #sets the coordinates of the closest piece of food within view
    def look(self, foodList):
        self.nearestFoodDistance = self.viewDistance
        self.foodInView = 0
        self.upFood = 0
        self.downFood = 0
        self.leftFood = 0
        self.rightFood = 0
        #loop through all the food
        for food in foodList:
            distance = constants.WORLDSIZE
            
            distance = self.getDistance(self.rect.centerx, self.rect.centery, food.rect.centerx, food.rect.centery)

            if (distance < self.viewDistance and food.alive):
                self.foodInView += 1
                if (food.rect.centery < self.rect.centery):
                    self.upFood += 1
                elif (food.rect.centery > self.rect.centery):
                    self.downFood += 1
                elif (food.rect.centerx < self.rect.centerx):
                    self.leftFood += 1
                else:
                    self.rightFood +=1
                #if the food is within view 
                if (distance < self.nearestFoodDistance):        
                    self.nearestFoodDistance = distance    
                    self.nearestFoodX = food.rect.centerx
                    self.nearestFoodY = food.rect.centery
                    
        #if no food was in view set center as closest food
        if (self.foodInView == 0):
            self.nearestFoodDistance = self.getDistance(self.rect.centerx, self.rect.centery, 500, 500)
            self.nearestFoodX = constants.WORLDSIZE/2
            self.nearestFoodY = constants.WORLDSIZE/2

    #Override
    #check if food is touching creature, if it is, eat
    def checkEat(self, foodList):
        for food in foodList:
            if (self.rect.colliderect(food.rect)):
                self.eat(food)
                if(self.training == False):
                    food.fitness -= 10
                    food.rect.centerx = 0
                    food.rect.centery = 0
                    food.energy = 0
                    food.alive = False
                else:
                    foodList.remove(food)
                    break
        return foodList