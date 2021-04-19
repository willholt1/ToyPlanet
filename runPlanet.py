import pygame
import neat
import random

import constants
import Herbivore
import Predator
import Food

pygame.init()

screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

def runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig):
        
    #init NEAT
    herbivores = []
    predators = []

    allSprites = pygame.sprite.Group()

    herbivoreNet = neat.nn.FeedForwardNetwork.create(herbivoreGenome, herbivoreConfig)
    predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)

    #create herbivores
    for i in range(round(constants.POPULATION * 0.9)):
        x, y = randomXY()
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y, 2)
            
        herbivores.append(animat)
    
    #create predators
    for i in range(round(constants.POPULATION * 0.1)):
        x, y = randomXY()
        animat = Predator.Predator('sprites/creature_red.png', x, y, 1)
            
        predators.append(animat)

    foodList = []
    for i in range(constants.POPULATION * constants.FOODMULTIPLIER):
        foodList = runReplenishFood(foodList)

    ###########
    #Main loop#
    ###########
    running = True
    while running:
        #Events
        for event in pygame.event.get():
            #closing window
            if (event.type == pygame.QUIT):
                pygame.quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    running = False 
        
        #Update
        allSprites.empty()
        aliveCreatues = 0
        for herbivore in herbivores:
            output = herbivoreNet.activate(herbivore.getData())
            decision = output.index(max(output)) + 1
            foodList = herbivore.update(foodList, predators, decision)
            
            #check if alive
            if (herbivore.alive):
                aliveCreatues += 1
            else:
                print(herbivore.fitness)
                herbivores.remove(herbivore)

            #reproduce
            if (herbivore.energy > constants.HREPRODUCTIONTHRESHOLD):
                x = herbivore.rect.centerx + 20
                y = herbivore.rect.centery + 20
                animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y, 2)
                herbivores.append(animat)
                herbivore.energy = herbivore.energy / 2
                herbivore.children += 1
            
        for predator in predators:
            output = predatorNet.activate(predator.getData())
            decision = output.index(max(output)) + 1
            herbivores = predator.update(herbivores, decision)
            
            #check if alive
            if (predator.alive):
                aliveCreatues += 1
            else:
                predators.remove(predator)

            #reproduce
            
            if (predator.energy > constants.PREPRODUCTIONTHRESHOLD):
                x = herbivore.rect.centerx + 20
                y = herbivore.rect.centery + 20
                animat = Predator.Predator('sprites/creature_red.png', x, y, 1)
                predators.append(animat)
                predator.energy = predator.energy / 2
                predator.children += 1
            
        if (aliveCreatues == 0):
            running = False
        
        #chance more food is generated. if more creatures, greater chance for food to be generated
        #if (random.randint(0,100) < (30 - round(len(herbivores)/4))) and (len(foodList) < 500):
        if (random.randint(0,100) < constants.FOODRESPAWN):
            foodList = runReplenishFood(foodList)

        allSprites.add(foodList, herbivores, predators)

        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(constants.FPS)

def randomXY():
    x = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))
    y = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))

    return x, y

def runReplenishFood(foodList):
    clusterX, clusterY = randomXY()
    for i in range(random.randint(1, constants.FOODCLUMPSIZE)):
        x = clusterX + random.randint(-constants.FOODDENSITY, constants.FOODDENSITY)
        y = clusterY + random.randint(-constants.FOODDENSITY, constants.FOODDENSITY)
        foodSprite = Food.Food('sprites/plant.png', x, y)
        foodList.append(foodSprite)
    return foodList