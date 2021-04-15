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

class Herbivore(Creature.Creature):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)

        self.nearestPredatorDistance = 1000
        self.nearestPredatorX = 0
        self.nearestPredatorY = 0
        self.predatorsInView = 0

        self.upPredator = 0
        self.downPredator = 0
        self.leftPredator = 0
        self.rightPredator = 0

    #Override
    def update(self, foodList, predators, action):
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

            Creature.Creature.look(self, foodList)
            self.lookPredators(predators)
            foodList = Creature.Creature.checkEat(self, foodList)
            self.energy -= 1
        else:
            self.alive = False

        return foodList

    def lookPredators(self, predators):
        self.nearestPredatorDistance = self.viewDistance
        self.predatorsInView = 0
        self.upPredator = 0
        self.downPredator = 0
        self.leftPredator = 0
        self.rightPredator = 0

        #loop through all the predators
        for predator in predators:
            distance = WORLDSIZE
            distance = self.getDistance(self.rect.centerx, self.rect.centery, predator.rect.centerx, predator.rect.centery)

            if (distance < self.viewDistance):
                self.predatorsInView += 1
                '''
                if (predator.rect.centery < self.rect.centery):
                    self.upPredator += 1
                elif (predator.rect.centery > self.rect.centery):
                    self.downPredator += 1
                elif (predator.rect.centerx < self.rect.centerx):
                    self.leftPredator += 1
                else:
                    self.rightPredator +=1
                '''

                #if the food is within view 
                if (distance < self.nearestPredatorDistance):
                    self.nearestPredatorDistance = distance
                    self.nearestPredatorX = predator.rect.centerx
                    self.nearestPredatorY = predator.rect.centery
                    
        #if no food was in view set center as closest food
        if (self.predatorsInView == 0):
            self.nearestPredatorDistance = self.getDistance(self.rect.centerx, self.rect.centery, 0, 0)
            self.nearestPredatorX = 500
            self.nearestPredatorY = 500

    #Override
    #data to be passed to the NN
    def getData(self):
        distanceFromTop = self.rect.centery
        distanceFromBottom = (1000 - self.rect.centery)
        distanceFromLeft = self.rect.centerx
        distanceFromRight = (1000 - self.rect.centerx)

        predatorUp = 1000
        predatorDown = 1000
        predatorLeft = 1000
        predatorRight = 1000

        if (self.nearestPredatorDistance < 50):
            predatorXdif = self.nearestPredatorX - self.rect.centerx
            predatorYdif = self.nearestPredatorY - self.rect.centery
            if (predatorXdif < 0):
                predatorLeft = predatorXdif * -1
                predatorRight = 1000
            else:
                predatorRight = predatorXdif
                predatorLeft = 1000

            if (predatorYdif < 0):
                predatorUp = predatorYdif * -1
                predatorDown = 1000
            else:
                predatorDown = predatorYdif
                predatorUp = 1000

        if (self.direction == UP):
            A = (0, -1)
            distanceFromCreatureForward = distanceFromTop
            distanceFromCreatureLeft = distanceFromLeft
            distanceFromCreatureRight = distanceFromRight
            foodForward = self.upFood
            foodLeft = self.leftFood
            foodRight = self.rightFood
            predatorDistanceForward = predatorUp
            predatorDistanceLeft = predatorLeft
            predatorDistanceRight = predatorRight
        elif (self.direction == DOWN):
            A = (0, 1)
            distanceFromCreatureForward = distanceFromBottom
            distanceFromCreatureLeft = distanceFromRight
            distanceFromCreatureRight = distanceFromLeft
            foodForward = self.downFood
            foodLeft = self.rightFood
            foodRight = self.leftFood
            predatorDistanceForward = predatorDown
            predatorDistanceLeft = predatorRight
            predatorDistanceRight = predatorLeft
        elif (self.direction == LEFT):
            A = (-1, 0)
            distanceFromCreatureForward = distanceFromLeft
            distanceFromCreatureLeft = distanceFromBottom
            distanceFromCreatureRight = distanceFromTop
            foodForward = self.leftFood
            foodLeft = self.downFood
            foodRight = self.upFood
            predatorDistanceForward = predatorLeft
            predatorDistanceLeft = predatorDown
            predatorDistanceRight = predatorUp
        else:
            A = (1, 0)
            distanceFromCreatureForward = distanceFromRight
            distanceFromCreatureLeft = distanceFromTop
            distanceFromCreatureRight = distanceFromBottom
            foodForward = self.rightFood
            foodLeft = self.upFood
            foodRight = self.downFood
            predatorDistanceForward = predatorRight
            predatorDistanceLeft = predatorUp
            predatorDistanceRight = predatorDown

        B = Creature.Creature.getVectors(self, self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY)
        
        angleToFood = Creature.Creature.angleBetween(self, A, B)
        angleToFood = Creature.Creature.adjustAngle(self, angleToFood)

        B = Creature.Creature.getVectors(self, self.rect.centerx, self.rect.centery, self.nearestPredatorX, self.nearestPredatorY)

        angleToPredator = Creature.Creature.angleBetween(self, A, B)
        angleToPredator = Creature.Creature.adjustAngle(self, angleToPredator)

        return [self.nearestFoodDistance,
                angleToFood,
                foodForward,
                foodLeft,
                foodRight,
                self.nearestPredatorDistance,
                angleToPredator, 
                predatorDistanceForward,
                predatorDistanceLeft,
                predatorDistanceRight,
                distanceFromCreatureForward,
                distanceFromCreatureLeft,
                distanceFromCreatureRight]
