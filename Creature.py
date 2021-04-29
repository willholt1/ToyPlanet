#################################################################
#Creature object, parent class to Herbivore and Predator classes#
#################################################################
#libraries
import pygame
import random
#classes
import Food
#misc
import constants
import utility

class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load(image).convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.training = False

        #creature attribute defaults
        self.speed = 1
        #inheritable attributes
        self.viewDistance = 250
        self.sleepTime = 150
        self.metabolism = 1

        #status variables
        self.direction = constants.UP
        self.energy = 800
        self.alive = True
        self.fitness = 0
        self.sleepCounter = 0

        #creature sensory data - used for NN
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
        self.children = 0

    #move creature forward in whatever direction it is facing
    def move(self):
        if (self.direction == constants.UP and self.rect.centery > 5):
            self.rect.centery -= self.speed
            self.distanceTravelled += self.speed
        elif (self.direction == constants.DOWN and self.rect.centery < (constants.WORLDSIZE - 5)):
            self.rect.centery += self.speed
            self.distanceTravelled += self.speed
        elif (self.direction == constants.LEFT and self.rect.centerx > 5):
            self.rect.centerx -= self.speed
            self.distanceTravelled += self.speed
        elif (self.direction == constants.RIGHT and self.rect.centerx < (constants.WORLDSIZE - 5)):
            self.rect.centerx += self.speed
            self.distanceTravelled += self.speed
        else:
            #decrease fitness and kill if move is invalid
            self.fitness -= 10
            self.energy = 0
            self.alive = False

    #rotate creature 90 degrees to the left
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
    
    #rotate creature 90 degrees to the right
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
            
            distance = utility.getDistance(self.rect.centerx, self.rect.centery, food.rect.centerx, food.rect.centery)

            if (distance < self.viewDistance):
                self.foodInView += 1
                if (food.rect.centery < self.rect.centery):
                    self.upFood += 1
                if (food.rect.centery > self.rect.centery):
                    self.downFood += 1
                if (food.rect.centerx < self.rect.centerx):
                    self.leftFood += 1
                if (food.rect.centerx > self.rect.centery):
                    self.rightFood +=1

                #if the food is within view 
                if (distance < self.nearestFoodDistance):        
                    self.nearestFoodDistance = distance    
                    self.nearestFoodX = food.rect.centerx
                    self.nearestFoodY = food.rect.centery
                    
        #if no food was in view set center as closest food
        if (self.foodInView == 0):
            self.nearestFoodDistance = utility.getDistance(self.rect.centerx, self.rect.centery, 750, 750)
            self.nearestFoodX = 500
            self.nearestFoodY = 500

    #init inheritable attributes to random numbers
    def randInheritValues(self):
        self.viewDistance = random.randint(constants.VIEWDISTANCEMIN, constants.VIEWDISTANCEMAX)
        self.sleepTime = random.randint(constants.SLEEPTIMEMIN, constants.SLEEPTIMEMAX)
        self.metabolism = random.randint(constants.METABOLISMMIN, constants.METABOLISMMAX)
    
    #inherit properties from parent and then mutate them
    def inherit(self, vd, st, m):
        self.viewDistance = vd
        self.sleepTime = st
        self.metabolism = m
        self.mutate()

    #mutate inheritable variables
    def mutate(self):
        mutated = False

        while (not mutated):
            selectMutation = random.randint(0,3)
            mutationAmmount = random.randint(-1, 1)

            if (selectMutation == 0):
                mutatedVal = round(self.viewDistance + (mutationAmmount * 10))
                if (constants.VIEWDISTANCEMIN >= mutatedVal >= constants.VIEWDISTANCEMAX):
                    self.viewDistance = mutatedVal
                    mutated = True
            elif (selectMutation == 1):
                mutatedVal = round(self.sleepTime + (mutationAmmount * 10))
                if (constants.SLEEPTIMEMIN >= mutatedVal >= constants.SLEEPTIMEMAX):
                    self.sleepTime = mutatedVal
                    mutated = True
            elif (selectMutation == 2):
                mutatedVal = round(self.metabolism + mutationAmmount)
                if (constants.METABOLISMMIN >= mutatedVal >= constants.METABOLISMMAX):
                    self.metabolism = mutatedVal
                    mutated = True
            elif (selectMutation == 3):
                mutated = True
