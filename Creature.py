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
LOOK = 4

class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load(image).convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.direction = UP
        self.energy = 1000
        self.speed = 1
        self.viewDistance = 100
        self.alive = True

        #creature memory
        self.nearestFoodX = WORLDSIZE/2
        self.nearestFoodY = WORLDSIZE/2

        #performance stats
        self.distanceTravelled = 0
        self.foodEaten = 0 
        self.freeMoves = 0
        self.children = 0

    def getData(self):
        return[self.rect.centerx, self.rect.centery, self.nearestFoodX, self.nearestFoodY, self.direction]

    def mutate(self):
        pass

    def createValues(self):
        pass
    
    def update(self, foodList, action):
        
        if (self.energy > 0):
            if (action == MOVE):
                self.move()
            elif (action == TURNLEFT):
                self.turnLeft()
            elif (action == TURNRIGHT):
                self.turnRight()
            elif (action == LOOK):
                self.look(foodList)
            self.energy -= 1
        else:
            self.alive = False

        foodList = self.checkEat(foodList)

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

    def checkEat(self, foodList):
        for food in foodList:
            if (self.rect.colliderect(food.rect)):
                self.eat(food)
                foodList.remove(food)
                break
        return foodList


    def eat(self, food):
        #increase energy by nutrition value of the food
        self.energy += food.energy
        self.foodEaten += 1

    #sets the coordinates of the closest piece of food within view
    def look(self, foodList):
        shortestDistance = WORLDSIZE
        for food in foodList:
            distance = self.getDistance(self.rect.centerx, self.rect.centery, food.rect.centerx, food.rect.centery)
            if ((distance < self.viewDistance) and (distance < shortestDistance)):
                shortestDistance = distance        
                self.nearestFoodX = food.rect.centerx
                self.nearestFoodY = food.rect.centery
            elif (shortestDistance == WORLDSIZE):
                self.nearestFoodX = WORLDSIZE/2
                self.nearestFoodY = WORLDSIZE/2
        #print('({}, {})'.format(self.nearestFoodX, self.nearestFoodY))

    def getInfo(self):
        print ('Energy = {} \n \
                Speed = {} \n \
                BaseEnergy = {} \n \
                ViewDistance = {} \n \
                MovementEfficiency = {} \n \
                FoodEaten = {} \n \
                DistanceTravelled = {} \n \
                FreeMoves = {} \n \
                Children = {} \n \
                Fitness = {}\n'\
                .format(self.energy,\
                        self.speed, \
                        self.baseEnergy,\
                        self.viewDistance,\
                        self.movementEfficiency,\
                        self.foodEaten,\
                        self.distanceTravelled,\
                        self.freeMoves,\
                        self.children,\
                        ((self.foodEaten + 1) * self.distanceTravelled)))
    
    def getFitness(self):
        #fitness = (self.foodEaten + 1) * self.distanceTravelled
        fitness = self.foodEaten
        print(fitness)
        if (self.speed == 1):
            f = open('dataOutput/HerbivoreStat.txt', 'a+')
            f.write('{}\n'.format(fitness))
            f.close()
        else:
            f = open('dataOutput/PredatorStat.txt', 'a+')
            f.write('{}\n'.format(fitness))
            f.close()

    def getPosition(self):
       print('x = {} & y = {}'.format(self.rec.centerx, self.rect.centery))
    
    def getDistance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
