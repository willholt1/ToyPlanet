#libraries
import pygame
import neat
import random
import csv
import os
#classes
import Herbivore
import Predator
import Food
#misc
import constants
import utility

#setup pygame window
pygame.init()
screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

#declare font
fontSmall = pygame.font.SysFont('timesnewroman', 14)

def runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig):
    #data output files
    #delete files if they already exist
    if (os.path.isfile('dataOutput/HerbivoreData.csv')):
        os.remove('dataOutput/HerbivoreData.csv')
    if (os.path.isfile('dataOutput/PredatorData.csv')):
        os.remove('dataOutput/PredatorData.csv')
    if (os.path.isfile('dataOutput/PopulationData.csv')):   
        os.remove('dataOutput/PopulationData.csv')

    #create files
    f = open('dataOutput/HerbivoreData.csv', 'x')
    f.close()
    f = open('dataOutput/PredatorData.csv', 'x')
    f.close()
    f = open('dataOutput/PopulationData.csv', 'x')
    f.close()
    popDataCount = 0

    #label columns
    with open('dataOutput/HerbivoreData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['fitness',
                         'foodEaten',
                         'distanceTravelled',
                         'children',
                         'viewDistance',
                         'sleepTime',
                         'metabolism'])

    with open('dataOutput/PredatorData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['fitness',
                         'foodEaten',
                         'distanceTravelled',
                         'children',
                         'viewDistance',
                         'sleepTime',
                         'metabolism'])

    with open('dataOutput/PopulationData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['plants',
                         'herbivores',
                         'predators'])

    #init NEAT
    herbivores = []
    predators = []
    constants.HTRAINPREDATORMOVE = True
    allSprites = pygame.sprite.Group()

    herbivoreNet = neat.nn.FeedForwardNetwork.create(herbivoreGenome, herbivoreConfig)
    predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)

    #create herbivores
    for i in range(round(constants.POPULATION * 0.8)):
        x, y = utility.randomXY()
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y)
        animat.randInheritValues()
        herbivores.append(animat)
    
    #create predators
    for i in range(round(constants.POPULATION * 0.2)):
        x, y = utility.randomXY()
        animat = Predator.Predator('sprites/creature_red.png', x, y)
        animat.randInheritValues()
        predators.append(animat)

    #generate food
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
        #update herbivores
        for herbivore in herbivores:
            #run NN and update herbivore
            output = herbivoreNet.activate(herbivore.getData())
            decision = output.index(max(output)) + 1
            foodList = herbivore.update(foodList, predators, decision)
            
            #check if alive, if dead write data to file
            if (herbivore.alive):
                aliveCreatues += 1
            else:
                with open('dataOutput/HerbivoreData.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([herbivore.fitness,
                                     herbivore.foodEaten,
                                     herbivore.distanceTravelled,
                                     herbivore.children,
                                     herbivore.viewDistance,
                                     herbivore.sleepTime,
                                     herbivore.metabolism])
                herbivores.remove(herbivore)

            #reproduce and pass values to child
            if (herbivore.energy > constants.HREPRODUCTIONTHRESHOLD):
                x = herbivore.rect.centerx
                y = herbivore.rect.centery
                animat = Herbivore.Herbivore('sprites/egg_blue.png', x, y)
                animat.inherit(herbivore.viewDistance, herbivore.sleepTime, herbivore.metabolism)
                animat.energy = herbivore.energy / 2
                herbivores.append(animat)
                herbivore.energy = herbivore.energy / 2
                herbivore.children += 1

        #update predators
        for predator in predators:
            #run NN and update predator
            output = predatorNet.activate(predator.getData())
            decision = output.index(max(output)) + 1
            herbivores = predator.update(herbivores, decision)
            
            #check if alive, if dead write data to file
            if (predator.alive):
                aliveCreatues += 1
            else:
                with open('dataOutput/PredatorData.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([predator.fitness,
                                     predator.foodEaten,
                                     predator.distanceTravelled,
                                     predator.children,
                                     predator.viewDistance,
                                     predator.sleepTime,
                                     predator.metabolism])
                predators.remove(predator)

            #reproduce and pass values to child
            if (predator.energy > constants.PREPRODUCTIONTHRESHOLD):
                x = predator.rect.centerx
                y = predator.rect.centery
                animat = Predator.Predator('sprites/egg_pink.png', x, y)
                animat.inherit(predator.viewDistance, predator.sleepTime, predator.metabolism)
                animat.energy = predator.energy / 2
                predators.append(animat)
                predator.energy = predator.energy / 2
                predator.children += 1
        
        #every 50 frames save population data to a file
        popDataCount += 1
        if (popDataCount > 50):
            with open('dataOutput/PopulationData.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([len(foodList), len(herbivores), len(predators)])
            popDataCount = 0

        if (aliveCreatues == 0):
            running = False
        
        #generate more food
        if (random.randint(0,100) < constants.FOODRESPAWN):
            foodList = runReplenishFood(foodList)

        allSprites.add(foodList, herbivores, predators)

        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)

        #display ammount of food
        foodCount = 'Food count: '+str(len(foodList))
        img = fontSmall.render(foodCount, True, (0,0,0))
        screen.blit(img, (10, 930))
        #display herbivore population
        hPop = 'H population: '+str(len(herbivores))
        img = fontSmall.render(hPop, True, (0,0,0))
        screen.blit(img, (10, 950))
        #display predator population
        pPop = 'P population: '+str(len(predators))
        img = fontSmall.render(pPop, True, (0,0,0))
        screen.blit(img, (10, 970))

        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(constants.FPS)

#function to generate food in clumps
def runReplenishFood(foodList):
    clusterX, clusterY = utility.randomXY()
    for i in range(random.randint(1, constants.FOODCLUMPSIZE)):
        x = clusterX + random.randint(-constants.FOODDENSITY, constants.FOODDENSITY)
        y = clusterY + random.randint(-constants.FOODDENSITY, constants.FOODDENSITY)
        foodSprite = Food.Food('sprites/plant.png', x, y)
        foodList.append(foodSprite)
    return foodList