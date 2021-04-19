import Food
import Creature
import constants
import random
import math
import numpy as np
import pygame

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
            if (action == constants.MOVE):
                Creature.Creature.move(self)
            elif (action == constants.TURNLEFT):
                Creature.Creature.turnLeft(self)
                Creature.Creature.move(self)
            elif (action == constants.TURNRIGHT):
                Creature.Creature.turnRight(self)
                Creature.Creature.move(self)

            Creature.Creature.look(self, foodList)
            self.lookPredators(predators)
            foodList = Creature.Creature.checkEat(self, foodList)

            self.energy -= 1
        else:
            if (self.foodEaten == 0):
                self.fitness -= 10
            self.rect.centerx = 0
            self.rect.centery = 0
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
            distance = constants.WORLDSIZE
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

                if (distance < self.nearestPredatorDistance):
                    self.nearestPredatorDistance = distance
                    self.nearestPredatorX = predator.rect.centerx
                    self.nearestPredatorY = predator.rect.centery
                    
        #if no food was in view set center as closest food
        if (self.predatorsInView == 0):
            self.nearestPredatorDistance = self.getDistance(self.rect.centerx, self.rect.centery, 0, 0)
            self.nearestPredatorX = 0
            self.nearestPredatorY = 0

    #Override
    #data to be passed to the NN
    def getData(self):
        distanceFromTop = self.rect.centery
        distanceFromBottom = (1000 - self.rect.centery)
        distanceFromLeft = self.rect.centerx
        distanceFromRight = (1000 - self.rect.centerx)

        predatorUp = self.viewDistance
        predatorDown = self.viewDistance
        predatorLeft = self.viewDistance
        predatorRight = self.viewDistance

        #in view up
        if (((self.rect.centery - self.viewDistance) <= self.nearestPredatorY <= self.rect.centery) and ((self.rect.centerx - 10) <= self.nearestPredatorX <= (self.rect.centerx + 10))):
            predatorUp = self.rect.centery - self.nearestPredatorY
            if (predatorUp < 0):
                predatorUp = predatorUp * -1
        #in view down
        elif ((self.rect.centery <= self.nearestPredatorY <= (self.rect.centery + self.viewDistance)) and ((self.rect.centerx - 10) <= self.nearestPredatorX <= (self.rect.centerx + 10))):
            predatorDown = self.rect.centery - self.nearestPredatorY
            if (predatorDown < 0):
                predatorDown = predatorDown * -1
        #in view left
        elif (((self.rect.centerx - self.viewDistance) <= self.nearestPredatorX <= self.rect.centerx) and ((self.rect.centery - 10) <= self.nearestPredatorY <= (self.rect.centery + 10))):
            predatorLeft = self.rect.centerx - self.nearestPredatorX
            if (predatorLeft < 0):
                predatorLeft = predatorLeft * -1
        #in view right
        elif ((self.rect.centerx <= self.nearestPredatorX <= (self.rect.centerx + self.viewDistance)) and ((self.rect.centery - 10) <= self.nearestPredatorY <= (self.rect.centery + 10))):
            predatorRight = self.rect.centerx - self.nearestPredatorX
            if (predatorRight < 0):
                predatorRight = predatorRight * -1
        
        if (self.direction == constants.UP):
            A = (0, -1)
            distanceFromCreatureForward = distanceFromTop
            distanceFromCreatureLeft = distanceFromLeft
            distanceFromCreatureRight = distanceFromRight
            foodForward = self.upFood
            foodLeft = self.leftFood
            foodRight = self.rightFood
            predatorRelativeForward = predatorUp
            predatorRelativeLeft = predatorLeft
            predatorRelativeRight = predatorRight
        elif (self.direction == constants.DOWN):
            A = (0, 1)
            distanceFromCreatureForward = distanceFromBottom
            distanceFromCreatureLeft = distanceFromRight
            distanceFromCreatureRight = distanceFromLeft
            foodForward = self.downFood
            foodLeft = self.rightFood
            foodRight = self.leftFood
            predatorRelativeForward = predatorDown
            predatorRelativeLeft = predatorRight
            predatorRelativeRight = predatorLeft
        elif (self.direction == constants.LEFT):
            A = (-1, 0)
            distanceFromCreatureForward = distanceFromLeft
            distanceFromCreatureLeft = distanceFromBottom
            distanceFromCreatureRight = distanceFromTop
            foodForward = self.leftFood
            foodLeft = self.downFood
            foodRight = self.upFood
            predatorRelativeForward = predatorLeft
            predatorRelativeLeft = predatorDown
            predatorRelativeRight = predatorUp
        else:
            A = (1, 0)
            distanceFromCreatureForward = distanceFromRight
            distanceFromCreatureLeft = distanceFromTop
            distanceFromCreatureRight = distanceFromBottom
            foodForward = self.rightFood
            foodLeft = self.upFood
            foodRight = self.downFood
            predatorRelativeForward = predatorRight
            predatorRelativeLeft = predatorUp
            predatorRelativeRight = predatorDown

        B = Creature.Creature.getVectors(self, self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY)
        
        angleToFood = Creature.Creature.angleBetween(self, A, B)
        angleToFood = Creature.Creature.adjustAngle(self, angleToFood)

        B = Creature.Creature.getVectors(self, self.rect.centerx, self.rect.centery, self.nearestPredatorX, self.nearestPredatorY)

        angleToPredator = Creature.Creature.angleBetween(self, A, B)
        angleToPredator = Creature.Creature.adjustAngle(self, angleToPredator)

        return [self.nearestFoodDistance,       #distance in pixels to the nearest piece of food
                angleToFood,                    #angle in degrees to the nearest piece of food relative to the creature
                foodForward,                    #amount of food in front of the creature
                foodLeft,                       #amount of food to the left of the creature
                foodRight,                      #amount of food to the right of the creature
                self.nearestPredatorDistance,   #distance in pixels to the nearest predator
                angleToPredator,                #angle in degrees to the nearest predator relative to the creature
                predatorRelativeForward,        #is there a predator in front
                predatorRelativeLeft,           #is there a predator to the left
                predatorRelativeRight,          #is there a predator to the right
                distanceFromCreatureForward,    #distance from the wall forward
                distanceFromCreatureLeft,       #distance from the wall left
                distanceFromCreatureRight]      #distance from the wall right
