import Food
import constants
import random
import math
import numpy as np
import pygame

class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load(image).convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.training = False
        #creature attributes
        self.speed = speed
        self.viewDistance = 250

        #status variables
        self.direction = constants.UP
        self.energy = 800
        self.alive = True
        self.fitness = 0

        #creature memory
        self.nearestFoodX = constants.WORLDSIZE/2
        self.nearestFoodY = constants.WORLDSIZE/2
        self.nearestFoodDistance = 0
        self.foodInView = 0
        self.upFood = 0
        self.downFood = 0
        self.leftFood = 0
        self.rightFood = 0

        #performance stats
        self.distanceTravelled = 0
        self.foodEaten = 0 
        self.freeMoves = 0
        self.children = 0

    def move(self):
        if (self.direction == constants.UP and self.rect.centery > 5):
            self.rect.centery -= self.speed
            self.distanceTravelled += 1
        elif (self.direction == constants.DOWN and self.rect.centery < (constants.WORLDSIZE - 5)):
            self.rect.centery += self.speed
            self.distanceTravelled += 1
        elif (self.direction == constants.LEFT and self.rect.centerx > 5):
            self.rect.centerx -= self.speed
            self.distanceTravelled += 1
        elif (self.direction == constants.RIGHT and self.rect.centerx < (constants.WORLDSIZE - 5)):
            self.rect.centerx += self.speed
            self.distanceTravelled += 1
        else:
            #decrease fitness if move is invalid
            self.fitness -= 10
            self.alive = False

    def turnLeft(self):
        if (self.direction == constants.UP):
            self.direction = constants.LEFT
        elif (self.direction == constants.LEFT):
            self.direction = constants.DOWN
        elif (self.direction == constants.DOWN):
            self.direction = constants.RIGHT
        else:
            self.direction = constants.UP

        self.image = pygame.transform.rotate(self.originalImage, self.direction)
            
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def turnRight(self):
        if (self.direction == constants.UP):
            self.direction = constants.RIGHT
        elif (self.direction == constants.RIGHT):
            self.direction = constants.DOWN
        elif (self.direction == constants.DOWN):
            self.direction = constants.LEFT
        else:
            self.direction = constants.UP
            
        self.image = pygame.transform.rotate(self.originalImage, self.direction)
        
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #check if food is touching creature, if it is, eat
    def checkEat(self, foodList):
        for food in foodList:
            if (self.rect.colliderect(food.rect)):
                self.eat(food)
                foodList.remove(food)
                break
        return foodList

    #increase energy by nutrition value of the food
    def eat(self, food):
        self.energy += food.energy
        self.foodEaten += 1
        self.fitness += 1

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

            if (distance < self.viewDistance):
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
            self.nearestFoodDistance = self.getDistance(self.rect.centerx, self.rect.centery, 750, 750)
            self.nearestFoodX = 500
            self.nearestFoodY = 500
            
    #calculate the distance between two points
    def getDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
    #calculate the angle between two vectors
    def angleBetween(self, p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    def getVectors(self, creatureX, creatureY, foodX, foodY):
        xVector = foodX - creatureX
        yVector = foodY - creatureY
        return (xVector, yVector)

    def adjustAngle(self, angle):
        if angle > 180:
            angle = 360 - angle
            angle = angle * -1
        return angle

    #data to be passed to the NN
    def getData(self):
        distanceFromTop = self.rect.centery
        distanceFromBottom = (1000 - self.rect.centery)
        distanceFromLeft = self.rect.centerx
        distanceFromRight = (1000 - self.rect.centerx)

        distanceFromCreatureForward = 0
        distanceFromCreatureLeft = 0
        distanceFromCreatureRight = 0

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

        B = self.getVectors(self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY)
            
        angle = self.angleBetween(A, B)

        angle = self.adjustAngle(angle)

        return[self.nearestFoodDistance, angle, foodForward, foodLeft, foodRight, distanceFromCreatureForward, distanceFromCreatureLeft, distanceFromCreatureRight]