############################
#class for predator sprites#
############################
#libraries
import pygame
import random
#classes
import Creature
import Food
#misc
import utility
import constants

class Predator(Creature.Creature):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = 1

    #Override
    def update(self, foodList, action):
        if (self.sleepCounter < self.sleepTime):
            self.sleepCounter += 1
            #hatch from egg
            if (self.sleepCounter == self.sleepTime):
                self.originalImage = pygame.image.load('sprites/creature_red.png').convert_alpha()
                self.image = self.originalImage
        else:
            #if set to be unable to move, just check for contact with food
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
                    self.energy -= self.metabolism
                else:
                    if (self.foodEaten == 0):
                        self.fitness -= 10
                    self.rect.centerx = 0
                    self.rect.centery = 0
                    self.alive = False
            else:
                foodList = self.checkEat(foodList)
        return foodList

    #override
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
            
            distance = utility.getDistance(self.rect.centerx, self.rect.centery, food.rect.centerx, food.rect.centery)

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
            self.nearestFoodDistance = utility.getDistance(self.rect.centerx, self.rect.centery, 500, 500)
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
                    #if the predator is training and therefore eating plants
                    foodList.remove(food)
                    break
        return foodList

    #data to be passed to the NN
    def getData(self):
        #calculate distance from the walls
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
        elif (self.direction == constants.DOWN):
            A = (0, 1)
            distanceFromCreatureForward = distanceFromBottom
            distanceFromCreatureLeft = distanceFromRight
            distanceFromCreatureRight = distanceFromLeft
            foodForward = self.downFood
            foodLeft = self.rightFood
            foodRight = self.leftFood
        elif (self.direction == constants.LEFT):
            A = (-1, 0)
            distanceFromCreatureForward = distanceFromLeft
            distanceFromCreatureLeft = distanceFromBottom
            distanceFromCreatureRight = distanceFromTop
            foodForward = self.leftFood
            foodLeft = self.downFood
            foodRight = self.upFood
        else:
            A = (1, 0)
            distanceFromCreatureForward = distanceFromRight
            distanceFromCreatureLeft = distanceFromTop
            distanceFromCreatureRight = distanceFromBottom
            foodForward = self.rightFood
            foodLeft = self.upFood
            foodRight = self.downFood

        #calculate angle to nearest piece of food
        B = utility.getVectors(self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY)
        angle = utility.angleBetween(A, B)
        angle = utility.adjustAngle(angle)

        return [self.nearestFoodDistance,           #distance in pixels to the nearest piece of food
                angle,                              #angle in degrees to the nearest piece of food relative to the creature
                foodForward,                        #amount of food in front of the creature
                foodLeft,                           #amount of food to the left of the creature
                foodRight,                          #amount of food to the right of the creature
                distanceFromCreatureForward,        #distance in pixels from the wall in front
                distanceFromCreatureLeft,           #distance in pixels from the wall left
                distanceFromCreatureRight]          #distance in pixels from the wall right