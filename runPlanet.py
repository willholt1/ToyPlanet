import pygame
import neat
import random
import csv
import constants
import Herbivore
import Predator
import Food
import os

pygame.init()

screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

fontSmall = pygame.font.SysFont('timesnewroman', 14)

def runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig):
    #data output files
    if (os.path.isfile('dataOutput/HerbivoreData.csv')):
        os.remove('dataOutput/HerbivoreData.csv')
    if (os.path.isfile('dataOutput/PredatorData.csv')):
        os.remove('dataOutput/PredatorData.csv')
    if (os.path.isfile('dataOutput/PopulationData.csv')):   
        os.remove('dataOutput/PopulationData.csv')

    f = open('dataOutput/HerbivoreData.csv', 'x')
    f.close()
    f = open('dataOutput/PredatorData.csv', 'x')
    f.close()
    f = open('dataOutput/PopulationData.csv', 'x')
    f.close()
    popDataCount = 0

    #init NEAT
    herbivores = []
    predators = []
    constants.HTRAINPREDATORMOVE = True
    allSprites = pygame.sprite.Group()

    herbivoreNet = neat.nn.FeedForwardNetwork.create(herbivoreGenome, herbivoreConfig)
    predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)

    #create herbivores
    for i in range(round(constants.POPULATION * 0.9)):
        x, y = randomXY()
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y)
        animat.randInheritValues()
        herbivores.append(animat)
    
    #create predators
    for i in range(round(constants.POPULATION * 0.1)):
        x, y = randomXY()
        animat = Predator.Predator('sprites/creature_red.png', x, y)
        animat.randInheritValues()
        predators.append(animat)

    foodList = []
    for i in range(constants.POPULATION):
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
                with open('dataOutput/HerbivoreData.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([herbivore.fitness, herbivore.foodEaten, herbivore.distanceTravelled, herbivore.children, herbivore.viewDistance, herbivore.sleepTime, herbivore.metabolism])
                herbivores.remove(herbivore)

            #reproduce
            if (herbivore.energy > constants.HREPRODUCTIONTHRESHOLD):
                x = herbivore.rect.centerx
                y = herbivore.rect.centery
                animat = Herbivore.Herbivore('sprites/egg_blue.png', x, y)
                animat.inherit(herbivore.viewDistance, herbivore.sleepTime, herbivore.metabolism)
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
                with open('dataOutput/PredatorData.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([predator.fitness, predator.foodEaten, predator.distanceTravelled, predator.children, predator.viewDistance, predator.sleepTime, predator.metabolism])
                predators.remove(predator)

            #reproduce
            if (predator.energy > constants.PREPRODUCTIONTHRESHOLD):
                x = herbivore.rect.centerx
                y = herbivore.rect.centery
                animat = Predator.Predator('sprites/egg_pink.png', x, y)
                animat.inherit(predator.viewDistance, predator.sleepTime, predator.metabolism)
                predators.append(animat)
                predator.energy = predator.energy / 2
                predator.children += 1
        
        popDataCount += 1
        if (popDataCount > 50):
            with open('dataOutput/PopulationData.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([len(foodList), len(herbivores), len(predators)])
            popDataCount = 0

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

        foodCount = 'Food count: '+str(len(foodList))
        img = fontSmall.render(foodCount, True, (0,0,0))
        screen.blit(img, (10, 930))

        hPop = 'H population: '+str(len(herbivores))
        img = fontSmall.render(hPop, True, (0,0,0))
        screen.blit(img, (10, 950))

        pPop = 'P population: '+str(len(predators))
        img = fontSmall.render(pPop, True, (0,0,0))
        screen.blit(img, (10, 970))

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