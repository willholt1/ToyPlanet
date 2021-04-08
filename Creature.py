import Food
import random
import math
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
        self.viewDistance = 200

        #status variables
        self.direction = UP
        self.energy = 500
        self.alive = True
        self.fitness = 0

        #creature memory
        self.nearestFoodX = WORLDSIZE/2
        self.nearestFoodY = WORLDSIZE/2
        self.nearestFoodDistance = 0
        self.lastNearestFoodDistance = 0
        self.lastDirection = self.direction
        self.lastDirectionCount = 0
        self.lastDistanceTravelled = 0
        self.lastDistanceTravelledCount = 0

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
            elif (action == TURNRIGHT):
                self.turnRight()

            self.lastDirectionCheck()
            self.distanceTravelledCheck()
            self.look(foodList)
            foodList = self.checkEat(foodList)
            self.energy -= 1
        else:
            self.alive = False
            if (self.distanceTravelled < 10):
                self.fitness -= 10
            else:
                self.fitness += self.foodEaten

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
            self.fitness -= 1


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

    #sets the coordinates of the closest piece of food within view
    def look(self, foodList):
        self.nearestFoodDistance = 500
        #loop through all the food
        for food in foodList:
            distance = WORLDSIZE
            #calculate distance if food is in front
            if ((self.direction == UP) and (food.rect.centery < self.rect.centery) or 
            ((self.direction == DOWN) and (food.rect.centery > self.rect.centery)) or 
            ((self.direction == LEFT) and (food.rect.centerx < self.rect.centerx)) or 
            ((self.direction == RIGHT) and (food.rect.centerx > self.rect.centerx))):
                #if food is in front, calculate distance
                distance = self.getDistance(self.rect.centerx, self.rect.centery, food.rect.centerx, food.rect.centery)

            #if the food is within view 
            if ((distance < self.viewDistance) and (distance < self.nearestFoodDistance)):        
                self.nearestFoodDistance = distance    
                self.nearestFoodX = food.rect.centerx
                self.nearestFoodY = food.rect.centery


        #if no food was in view set center as closest food
        if (self.nearestFoodDistance == WORLDSIZE):
            self.nearestFoodDistance = self.getDistance(self.rect.centerx, self.rect.centery, 500, 500)
            self.nearestFoodX = WORLDSIZE/2
            self.nearestFoodY = WORLDSIZE/2
        
        #if the creatue is closer to the nearest piece of food increase fitness, if it is further away then decrease
        if (self.nearestFoodDistance < self.lastNearestFoodDistance):
            self.fitness += 0.01
        else:
            self.fitness -= 0.01

        self.lastNearestFoodDistance = self.nearestFoodDistance

    #- fitness if creatures go in one direction for too long
    def lastDirectionCheck(self):
        if (self.direction == self.lastDirection):
            self.lastDirectionCount += 1
        else:
            self.lastDirectionCount = 0

        self.lastDirection = self.direction

        if (self.lastDirectionCount >= self.viewDistance):
            self.fitness -= 2

    def distanceTravelledCheck(self):
        if (self.distanceTravelled == self.lastDistanceTravelled):
            self.lastDistanceTravelledCount += 1
        else:
            self.lastDistanceTravelledCount = 0

        self.lastDistanceTravelled = self.distanceTravelled

        if (self.lastDistanceTravelledCount >= 15):
            self.fitness -= 2

    #calculate the distance between two points
    def getDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    #data to be passed to the NN
    def getData(self):
        foodXDifference = self.nearestFoodX - self.rect.centerx
        foodYDifference = self.nearestFoodY - self.rect.centery
        if (self.direction == UP):
            creatureXDirection = 0
            creatureYDirection = -1
        elif (self.direction == DOWN):
            creatureXDirection = 0
            creatureYDirection = 1
        elif (self.direction == LEFT):
            creatureXDirection = -1
            creatureYDirection = 0
        elif (self.direction == RIGHT):
            creatureXDirection = 1
            creatureYDirection = 0
        else:
            creatureXDirection = 0
            creatureYDirection = 0

        return[foodXDifference, foodYDifference, creatureXDirection, creatureYDirection]