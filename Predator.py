import Food
import Creature
import random
import math
import numpy as np
import pygame

UP = 0
DOWN = 180
LEFT = 90
RIGHT = 270

WORLDSIZE = 1000

MOVE = 1
TURNLEFT = 2
TURNRIGHT = 3

class Predator(Creature.Creature):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)

    #Override
    def update(self, foodList, action):
        if (self.energy > 0):
            #perform action determined by the NN
            if (action == MOVE):
                Creature.Creature.move(self)
            elif (action == TURNLEFT):
                Creature.Creature.turnLeft(self)
                Creature.Creature.move(self)
            elif (action == TURNRIGHT):
                Creature.Creature.turnRight(self)
                Creature.Creature.move(self)

            self.look(foodList)
            foodList = self.checkEat(foodList)
            self.energy -= 1
        else:
            self.alive = False

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
            distance = WORLDSIZE
            
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
            self.nearestFoodX = WORLDSIZE/2
            self.nearestFoodY = WORLDSIZE/2

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
                    food.alive = False
                else:
                    foodList.remove(food)
                break
        return foodList