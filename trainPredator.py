import pygame
import neat
import random
import pickle

import constants
import Herbivore
import Predator
import Food

pygame.init()

screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

def trainPredator(genomes, config):
    #init NEAT
    nets = []
    predators = []
    
    allSprites = pygame.sprite.Group()

    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = 500
        y = 500
        predator = Predator.Predator('sprites/creature_red.png', x, y, 1)
        predator.training = True
            
        predators.append(predator)
    
    foodList = []
    for i in range(constants.PTRAINFOODCOUNT):
        foodList = trainReplenishFood(foodList)

    lastFoodLen = len(foodList)
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
        for i, predator in enumerate(predators):  
            if (predator.alive):
                output = nets[i].activate(predator.getData())
                decision = output.index(max(output)) + 1
                foodList = predator.update(foodList, decision)
                genomes[i][1].fitness = predator.fitness
                aliveCreatues += 1

        if (aliveCreatues == 0):
            running = False

        if (len(foodList)< lastFoodLen):
            foodList = trainReplenishFood(foodList)
        
        lastFoodLen = len(foodList)

        allSprites.add(predators, foodList)
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(constants.FPS)

def trainReplenishFood(foodList):
    x, y = randomXY()
    
    foodSprite = Food.Food('sprites/plant.png', x, y)
    foodList.append(foodSprite)
    return foodList

def randomXY():
    x = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))
    y = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))

    return x, y