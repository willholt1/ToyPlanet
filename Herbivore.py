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

        self.nearestUpPredator = self.viewDistance
        self.nearestTopRightPredator = self.viewDistance
        self.nearestRightPredator = self.viewDistance
        self.nearestBottomRightPredator = self.viewDistance
        self.nearestTopLeftPredator = self.viewDistance
        self.nearestLeftPredator = self.viewDistance
        self.nearestBottomLeftPredator = self.viewDistance
        self.nearestBottomPredator = self.viewDistance

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
            self.energy = 0
            self.alive = False

        return foodList

    def lookPredators(self, predators):
        self.nearestPredatorDistance = self.viewDistance
        self.predatorsInView = 0
        self.nearestUpPredator = self.viewDistance
        self.nearestTopRightPredator = self.viewDistance
        self.nearestRightPredator = self.viewDistance
        self.nearestBottomRightPredator = self.viewDistance
        self.nearestTopLeftPredator = self.viewDistance
        self.nearestLeftPredator = self.viewDistance
        self.nearestBottomLeftPredator = self.viewDistance
        self.nearestBottomPredator = self.viewDistance

        #loop through all the predators
        for predator in predators:
            distance = constants.WORLDSIZE
            distance = self.getDistance(self.rect.centerx, self.rect.centery, predator.rect.centerx, predator.rect.centery)

            if (distance < self.viewDistance):
                A = (0, -1)
                B = Creature.Creature.getVectors(self, self.rect.centerx, self.rect.centery, predator.rect.centerx, predator.rect.centery)
        
                angleToPredator = Creature.Creature.angleBetween(self, A, B)
                angleToPredator = Creature.Creature.adjustAngle(self, angleToPredator)
                
                if ((-5 <= angleToPredator <= 5) and (distance < self.nearestUpPredator)):
                    self.nearestUpPredator = distance
                    #print("up")
                elif ((40 <= angleToPredator <= 50) and (distance < self.nearestTopRightPredator)):
                    self.nearestTopRightPredator = distance
                    #print("TR")
                elif ((85 <= angleToPredator <= 95) and (distance < self.nearestRightPredator)):
                    self.nearestRightPredator = distance
                    #print("R")
                elif ((130 <= angleToPredator <= 140) and (distance < self.nearestBottomRightPredator)):
                    self.nearestBottomRightPredator = distance
                    #print("BR")
                elif ((-50 <= angleToPredator <= -40) and (distance < self.nearestTopLeftPredator)):
                    self.nearestTopLeftPredator = distance
                    #print("TL")
                elif ((-95 <= angleToPredator <= -85) and (distance < self.nearestLeftPredator)):
                    self.nearestLeftPredator = distance
                    #print("L")
                elif ((-140 <= angleToPredator <= -130) and (distance < self.nearestBottomLeftPredator)):
                    self.nearestBottomLeftPredator = distance
                    #print("BL")
                elif (((angleToPredator < -175) or (angleToPredator > 175)) and (distance < self.nearestBottomPredator)):
                    self.nearestBottomPredator = distance
                    #print("B")

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

        if (self.direction == constants.UP):
            A = (0, -1)
            distanceFromCreatureForward = distanceFromTop
            distanceFromCreatureLeft = distanceFromLeft
            distanceFromCreatureRight = distanceFromRight
            foodForward = self.upFood
            foodLeft = self.leftFood
            foodRight = self.rightFood
            predatorRelativeForward = self.nearestUpPredator
            predatorRelativeTopRight = self.nearestTopRightPredator
            predatorRelativeRight = self.nearestRightPredator
            predatorRelativeBottomRight = self.nearestBottomRightPredator
            predatorRelativeTopLeft = self.nearestTopLeftPredator
            predatorRelativeLeft =  self.nearestLeftPredator
            predatorRelativeBottomLeft = self.nearestBottomLeftPredator
        elif (self.direction == constants.DOWN):
            A = (0, 1)
            distanceFromCreatureForward = distanceFromBottom
            distanceFromCreatureLeft = distanceFromRight
            distanceFromCreatureRight = distanceFromLeft
            foodForward = self.downFood
            foodLeft = self.rightFood
            foodRight = self.leftFood
            predatorRelativeForward = self.nearestBottomPredator
            predatorRelativeTopRight = self.nearestBottomLeftPredator
            predatorRelativeRight = self.nearestLeftPredator
            predatorRelativeBottomRight = self.nearestTopLeftPredator
            predatorRelativeTopLeft = self.nearestBottomRightPredator
            predatorRelativeLeft =  self.nearestRightPredator
            predatorRelativeBottomLeft = self.nearestTopRightPredator
        elif (self.direction == constants.LEFT):
            A = (-1, 0)
            distanceFromCreatureForward = distanceFromLeft
            distanceFromCreatureLeft = distanceFromBottom
            distanceFromCreatureRight = distanceFromTop
            foodForward = self.leftFood
            foodLeft = self.downFood
            foodRight = self.upFood
            predatorRelativeForward = self.nearestRightPredator
            predatorRelativeTopRight = self.nearestBottomRightPredator
            predatorRelativeRight = self.nearestBottomPredator
            predatorRelativeBottomRight = self.nearestBottomLeftPredator
            predatorRelativeTopLeft = self.nearestTopRightPredator
            predatorRelativeLeft =  self.nearestUpPredator
            predatorRelativeBottomLeft = self.nearestTopLeftPredator
        else:
            A = (1, 0)
            distanceFromCreatureForward = distanceFromRight
            distanceFromCreatureLeft = distanceFromTop
            distanceFromCreatureRight = distanceFromBottom
            foodForward = self.rightFood
            foodLeft = self.upFood
            foodRight = self.downFood
            predatorRelativeForward = self.nearestLeftPredator
            predatorRelativeTopRight = self.nearestTopLeftPredator
            predatorRelativeRight = self.nearestUpPredator
            predatorRelativeBottomRight = self.nearestTopRightPredator
            predatorRelativeTopLeft = self.nearestBottomLeftPredator
            predatorRelativeLeft =  self.nearestBottomPredator
            predatorRelativeBottomLeft = self.nearestBottomRightPredator

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
                predatorRelativeForward,
                predatorRelativeTopRight,
                predatorRelativeRight,
                predatorRelativeBottomRight,
                predatorRelativeTopLeft,
                predatorRelativeLeft,
                predatorRelativeBottomLeft, 
                distanceFromCreatureForward,    #distance from the wall forward
                distanceFromCreatureLeft,       #distance from the wall left
                distanceFromCreatureRight]      #distance from the wall right
