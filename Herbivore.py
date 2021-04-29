#########################################################################
#class for herbivore sprites - has functionality for detecting predators#
#########################################################################
#libraries
import pygame
import random
#classes
import Creature
import Food
#misc
import constants
import utility

class Herbivore(Creature.Creature):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        self.speed = 2

        #creature sensory data
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
            if (self.sleepCounter < self.sleepTime):
                self.sleepCounter += 1
                #hatch creature from egg
                if (self.sleepCounter == self.sleepTime):
                    self.originalImage = pygame.image.load('sprites/creature_blue.png').convert_alpha()
                    self.image = self.originalImage
            else:
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

                self.energy -= self.metabolism
        else:
            if (self.foodEaten == 0):
                self.fitness -= 10
            self.rect.centerx = 0
            self.rect.centery = 0
            self.energy = 0
            self.alive = False

        return foodList

    #loop through all the predators and set sensory data for the closest ones - similar to look function in Creature.py
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

        for predator in predators:
            distance = constants.WORLDSIZE
            distance = utility.getDistance(self.rect.centerx, self.rect.centery, predator.rect.centerx, predator.rect.centery)
            
            if (distance < self.viewDistance):
                self.predatorsInView += 1
                A = (0, -1)
                B = utility.getVectors(self.rect.centerx, self.rect.centery, predator.rect.centerx, predator.rect.centery)
        
                angleToPredator = utility.angleBetween(A, B)
                angleToPredator = utility.adjustAngle(angleToPredator)
                
                #up
                if ((-5 <= angleToPredator <= 5) and (distance < self.nearestUpPredator)):
                    self.nearestUpPredator = distance
                #top right
                elif ((40 <= angleToPredator <= 50) and (distance < self.nearestTopRightPredator)):
                    self.nearestTopRightPredator = distance
                #right
                elif ((85 <= angleToPredator <= 95) and (distance < self.nearestRightPredator)):
                    self.nearestRightPredator = distance
                #bottom right
                elif ((130 <= angleToPredator <= 140) and (distance < self.nearestBottomRightPredator)):
                    self.nearestBottomRightPredator = distance
                #top left
                elif ((-50 <= angleToPredator <= -40) and (distance < self.nearestTopLeftPredator)):
                    self.nearestTopLeftPredator = distance
                #left
                elif ((-95 <= angleToPredator <= -85) and (distance < self.nearestLeftPredator)):
                    self.nearestLeftPredator = distance
                #bottom left
                elif ((-140 <= angleToPredator <= -130) and (distance < self.nearestBottomLeftPredator)):
                    self.nearestBottomLeftPredator = distance
                #bottom
                elif (((angleToPredator < -175) or (angleToPredator > 175)) and (distance < self.nearestBottomPredator)):
                    self.nearestBottomPredator = distance

                
                if (distance < self.nearestPredatorDistance):
                    self.nearestPredatorDistance = distance
                    self.nearestPredatorX = predator.rect.centerx
                    self.nearestPredatorY = predator.rect.centery
                    
        #if no food was in view set center as closest food
        if (self.predatorsInView == 0):
            self.nearestPredatorDistance = utility.getDistance(self.rect.centerx, self.rect.centery, 0, 0)
            self.nearestPredatorX = 0
            self.nearestPredatorY = 0

    #data to be passed to the NN
    def getData(self):
        #calculate distances from the walls
        distanceFromTop = self.rect.centery
        distanceFromBottom = (1000 - self.rect.centery)
        distanceFromLeft = self.rect.centerx
        distanceFromRight = (1000 - self.rect.centerx)

        #convert all creature sensory data to be relative to the direction it is facing
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

        #calculate angle to nearest piece of food
        B = utility.getVectors(self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY)
        angleToFood = utility.angleBetween(A, B)
        angleToFood = utility.adjustAngle(angleToFood)

        #calculate angle to nearest predator
        B = utility.getVectors(self.rect.centerx, self.rect.centery, self.nearestPredatorX, self.nearestPredatorY)
        angleToPredator = utility.angleBetween(A, B)
        angleToPredator = utility.adjustAngle(angleToPredator)
        #print(self.nearestPredatorDistance)
        return [self.nearestFoodDistance,       #distance in pixels to the nearest piece of food
                angleToFood,                    #angle in degrees to the nearest piece of food relative to the creature
                foodForward,                    #amount of food in front of the creature
                foodLeft,                       #amount of food to the left of the creature
                foodRight,                      #amount of food to the right of the creature
                self.nearestPredatorDistance,   #distance in pixels to the nearest predator
                angleToPredator,                #angle in degrees to the nearest predator relative to the creature
                predatorRelativeForward,        #distance in pixels to the nearest predator directly in front
                predatorRelativeTopRight,       #distance in pixels to the nearest predator to the top right
                predatorRelativeRight,          #distance in pixels to the nearest predator to the right
                predatorRelativeBottomRight,    #distance in pixels to the nearest predator to the bottom right
                predatorRelativeTopLeft,        #distance in pixels to the nearest predator to the top left
                predatorRelativeLeft,           #distance in pixels to the nearest predator to the left
                predatorRelativeBottomLeft,     #distance in pixels to the nearest predator to the bottom left
                distanceFromCreatureForward,    #distance in pixels from the wall in front
                distanceFromCreatureLeft,       #distance in pixels from the wall left
                distanceFromCreatureRight]      #distance in pixels from the wall right
