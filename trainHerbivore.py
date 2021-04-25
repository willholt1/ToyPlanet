###################################
#game loop for training herbivores#
###################################
#libraries
import pygame
import neat
import pickle
#classes
import Herbivore
import Predator
import Food
#misc
import utility
import constants

#setup pygame window
pygame.init()
screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()


def trainHerbivore(genomes, config):
    #init NEAT
    nets = []
    herbivores = []
    predators = []

    allSprites = pygame.sprite.Group()
    
    #if moving predators is set to true, load in predator brain
    if (constants.HTRAINPREDATORMOVE):
        configPathPredator = 'NEAT_configs/neat-config-predators.txt'
        predatorConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathPredator)
        # load predator genome
        with open("savedNNs/predator.pkl", "rb") as f:
            predatorGenome = pickle.load(f)
            f.close()
        #create predator brain
        predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)

    #create predators
    for i in range(constants.HTRAINPREDATORCOUNT):
        x, y = utility.randomXY()
        predator = Predator.Predator('sprites/creature_red.png', x, y)
        predator.viewDistance = 1500
        predators.append(predator)

    #create herbivores
    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = 500
        y = 500
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y)
        animat.training = True
        animat.sleepTime = 1
        herbivores.append(animat)
    
    #create food
    foodList = []
    for i in range(constants.HTRAINFOODCOUNT):
        foodList = utility.trainReplenishFood(foodList)

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
        #update herbivores
        for i, herbivore in enumerate(herbivores):
            if (herbivore.alive):
                #run data through NN
                output = nets[i].activate(herbivore.getData())
                #pass the highest weighted desicion to the update function of the sprite
                decision = output.index(max(output)) + 1
                foodList = herbivore.update(foodList, predators, decision)
                #update fitness
                genomes[i][1].fitness = herbivore.fitness
                aliveCreatues += 1

                #if food was eaten, generate more
                if (len(foodList)< lastFoodLen):
                    foodList = utility.trainReplenishFood(foodList)
        
                lastFoodLen = len(foodList)

        #if no more herbivores are alive, stop the generation
        if (aliveCreatues == 0):
            running = False

        #update predators
        for predator in predators:
            #only call NN if predator moving is set to true
            if (constants.HTRAINPREDATORMOVE):
                output = predatorNet.activate(predator.getData())
                decision = output.index(max(output)) + 1
            else:
                decision = 5
            herbivores = predator.update(herbivores, decision)
            predator.energy += 1

        allSprites.add(predators, herbivores, foodList)
        
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(constants.FPS)
############################END trainHerbivore############################
