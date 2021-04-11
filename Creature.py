import Food
import random
import math
import numpy as np
import pygame

#CONSTANTS
UP = 0
DOWN = 180
LEFT = 90
RIGHT = 270

WORLDSIZE = 1000

MOVE = 1
TURNLEFT = 2
TURNRIGHT = 3

class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load(image).convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        #creature attributes
        self.speed = 1
        self.viewDistance = 250

        #status variables
        self.direction = UP
        self.energy = 800
        self.alive = True
        self.fitness = 0

        #creature memory
        self.nearestFoodX = WORLDSIZE/2
        self.nearestFoodY = WORLDSIZE/2
        self.nearestFoodDistance = 0
        self.lastNearestFoodDistance = 0
        self.lastDirection = self.direction
        self.lastDirectionCount = 0
        #self.distanceFromSavedPoint = 0
        self.distanceFromSavedPointCount = 0
        self.savedPointX = self.rect.centerx
        self.savedPointY = self.rect.centery
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
    
    def update(self, foodList, action):
        if (self.energy > 0):
            #perform action determined by the NN
            if (action == MOVE):
                self.move()
            elif (action == TURNLEFT):
                self.turnLeft()
                self.move()
            elif (action == TURNRIGHT):
                self.turnRight()
                self.move()

            #self.lastDirectionCheck()
            #self.distanceTravelledCheck()
            self.look(foodList)
            foodList = self.checkEat(foodList)
            self.energy -= 1
        else:
            self.alive = False

        return foodList

    def move(self):
        if (self.direction == UP and self.rect.centery > 5):
            self.rect.centery -= self.speed
            self.distanceTravelled += 1
        elif (self.direction == DOWN and self.rect.centery < (WORLDSIZE - 5)):
            self.rect.centery += self.speed
            self.distanceTravelled += 1
        elif (self.direction == LEFT and self.rect.centerx > 5):
            self.rect.centerx -= self.speed
            self.distanceTravelled += 1
        elif (self.direction == RIGHT and self.rect.centerx < (WORLDSIZE - 5)):
            self.rect.centerx += self.speed
            self.distanceTravelled += 1
        else:
            #decrease fitness if move is invalid
            self.fitness -= 100
            self.alive = False

    def turnLeft(self):
        if (self.direction == UP):
            self.direction = LEFT
        elif (self.direction == LEFT):
            self.direction = DOWN
        elif (self.direction == DOWN):
            self.direction = RIGHT
        else:
            self.direction = UP

        self.image = pygame.transform.rotate(self.originalImage, self.direction)
            
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def turnRight(self):
        if (self.direction == UP):
            self.direction = RIGHT
        elif (self.direction == RIGHT):
            self.direction = DOWN
        elif (self.direction == DOWN):
            self.direction = LEFT
        else:
            self.direction = UP
            
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
        self.fitness += 10

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
            self.nearestFoodDistance = self.getDistance(self.rect.centerx, self.rect.centery, 500, 500)
            self.nearestFoodX = WORLDSIZE/2
            self.nearestFoodY = WORLDSIZE/2
        
        #if the creatue is closer to the nearest piece of food increase fitness, if it is further away then decrease
        #if (self.nearestFoodDistance < self.lastNearestFoodDistance):
        #    self.fitness += 0.01
        #else:
        #self.fitness -= 0.01

        self.lastNearestFoodDistance = self.nearestFoodDistance

    #- fitness if creatures go in one direction for too long
    def lastDirectionCheck(self):
        if (self.direction == self.lastDirection):
            self.lastDirectionCount += 1
        else:
            self.lastDirectionCount = 0

        self.lastDirection = self.direction

        if (self.lastDirectionCount >= self.viewDistance):
            self.fitness -= 1

    #anti spinning around
    def distanceTravelledCheck(self):
        distanceFromSavedPoint = self.getDistance(self.rect.centerx, self.rect.centery, self.savedPointX, self.savedPointY)
        
        if (distanceFromSavedPoint < 30):
            self.distanceFromSavedPointCount += 1
        else:
            self.distanceFromSavedPointCount = 0
            self.savedPointX = self.rect.centerx
            self.savedPointY = self.rect.centery
        
        if (self.distanceFromSavedPointCount > 60):
            self.fitness -= 1
            
    #calculate the distance between two points
    def getDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
    def angleBetween(self, p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    def getVectors(self, creatureX, creatureY, foodX, foodY):
        xVector = foodX - creatureX
        yVector = foodY - creatureY
        return (xVector, yVector)

    #data to be passed to the NN
    def getData(self):

        distanceFromTop = self.rect.centery
        distanceFromBottom = (1000 - self.rect.centery)
        distanceFromLeft = self.rect.centerx
        distanceFromRight = (1000 - self.rect.centerx)

        distanceFromCreatureForward = 0
        distanceFromCreatureLeft = 0
        distanceFromCreatureRight = 0

        if (self.direction == UP):
            A = (0, -1)
            distanceFromCreatureForward = distanceFromTop
            distanceFromCreatureLeft = distanceFromLeft
            distanceFromCreatureRight = distanceFromRight
            foodForward = self.upFood
            foodLeft = self.leftFood
            foodRight = self.rightFood
        elif (self.direction == DOWN):
            A = (0, 1)
            distanceFromCreatureForward = distanceFromBottom
            distanceFromCreatureLeft = distanceFromRight
            distanceFromCreatureRight = distanceFromLeft
            foodForward = self.downFood
            foodLeft = self.rightFood
            foodRight = self.leftFood
        elif (self.direction == LEFT):
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

        if angle > 180:
            angle = 360 - angle
            angle = angle * -1

        #angle = angle/180

        return[self.nearestFoodDistance, angle, foodForward, foodLeft, foodRight, distanceFromCreatureForward, distanceFromCreatureLeft, distanceFromCreatureRight]