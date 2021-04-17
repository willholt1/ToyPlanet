import pygame
import random
import Herbivore
import Predator
import Food
import neat
import pickle

WORLDSIZE = 1000
FPS = 1000

SPAWNBORDER = 50

POPULATION = 20
FOODDENSITY = 20
FOODMULTIPLIER = 1
FOODRESPAWN = 5
FOODCLUMPSIZE = 8

#0 = train predators
#1 = train herbivores
#2 = run planet
MODE = 1

def trainPredator(genomes, config):
    #init NEAT
    nets = []
    predators = []

    pygame.init()

    screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
    pygame.display.set_caption('Toy Planet')
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()


    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = 500
        y = 500
        predator = Predator.Predator('sprites/creature_red.png', x, y, 1)
            
        predators.append(predator)

    
    foodList = []
    for i in range(POPULATION * FOODMULTIPLIER):
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

        #Update
        allSprites.empty()
        aliveCreatues = 0
        for i, predator in enumerate(predators):
            output = nets[i].activate(predator.getData())
            decision = output.index(max(output)) + 1
            foodList = predator.update(foodList, decision)
            genomes[i][1].fitness = predator.fitness
            
            if (predator.alive):
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
        clock.tick(FPS)
############################END trainPredator############################

def trainHerbivore(genomes, config):
    
    #init NEAT
    nets = []
    herbivores = []
    predators = []

    pygame.init()

    screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
    pygame.display.set_caption('Toy Planet')
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()
    
    '''
    configPathPredator = './neat-config-predators.txt'

    predatorConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathPredator)
    # load predator genome
    with open("predator.pkl", "rb") as f:
        predatorGenome = pickle.load(f)
        f.close()
    #create predators
    predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)
    '''

    for i in range(15):
        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        predator = Predator.Predator('sprites/creature_red.png', x, y, 1)
        predators.append(predator)

    #create herbivores
    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = 500
        y = 500
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y, 2)
        animat.training = True
        #animat.viewDistance = 800
            
        herbivores.append(animat)

    
    foodList = []
    for i in range(30):
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

        #Update
        allSprites.empty()
        aliveCreatues = 0
        for i, herbivore in enumerate(herbivores):
            if (herbivore.alive):
                output = nets[i].activate(herbivore.getData())
                decision = output.index(max(output)) + 1
                foodList = herbivore.update(foodList, predators, decision)
                genomes[i][1].fitness = herbivore.fitness
                aliveCreatues += 1

                if (len(foodList)< lastFoodLen):
                    foodList = trainReplenishFood(foodList)
        
                lastFoodLen = len(foodList)

        if (aliveCreatues == 0):
            running = False

        for predator in predators:
            #output = predatorNet.activate(predator.getData())
            #decision = output.index(max(output)) + 1
            decision = 5
            herbivores = predator.update(herbivores, decision)

        

        allSprites.add(predators, herbivores, foodList)
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(FPS)
############################END trainHerbivore############################

def runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig):
        
    #init NEAT
    herbivores = []
    predators = []

    pygame.init()

    screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
    pygame.display.set_caption('Toy Planet')
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()

    herbivoreNet = neat.nn.FeedForwardNetwork.create(herbivoreGenome, herbivoreConfig)
    predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)

    #create herbivores
    for i in range(round(POPULATION * 0.9)):
        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y, 2)
            
        herbivores.append(animat)
    
    #create predators
    for i in range(round(POPULATION * 0.1)):
        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        animat = Predator.Predator('sprites/creature_red.png', x, y, 1)
            
        predators.append(animat)

    foodList = []
    for i in range(POPULATION * FOODMULTIPLIER):
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
                herbivores.remove(herbivore)

            #reproduce
            
            if (herbivore.energy > 1000):
                x = herbivore.rect.centerx + 10
                y = herbivore.rect.centery + 10
                animat = Herbivore.Herbivore('sprites/creature_blue.png', x, y, 2)
                herbivores.append(animat)
                herbivore.energy -= 300
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
            
            if (predator.energy > 1000000):
                x = herbivore.rect.centerx + 10
                y = herbivore.rect.centery + 10
                animat = Predator.Predator('sprites/creature_red.png', x, y, 1)
                predators.append(animat)
                predator.energy -= 300
                predator.children += 1
            
        if (aliveCreatues == 0):
            running = False
        
        #chance more food is generated. if more creatures, greater chance for food to be generated
        #(random.randint(0,100) < (30 - round(len(herbivores)/4))) and (len(foodList) < 500)
        if (random.randint(0,100) < FOODRESPAWN):
            foodList = runReplenishFood(foodList)

        allSprites.add(foodList, herbivores, predators)

        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(FPS)
############################END runPlanet############################

def runReplenishFood(foodList):
    clusterX = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    clusterY = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    for i in range(random.randint(1, FOODCLUMPSIZE)):
        x = clusterX + random.randint(-FOODDENSITY, FOODDENSITY)
        y = clusterY + random.randint(-FOODDENSITY, FOODDENSITY)
        foodSprite = Food.Food('sprites/plant.png', x, y)
        foodList.append(foodSprite)
    return foodList

def trainReplenishFood(foodList):
    clusterX = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    clusterY = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    x = clusterX + random.randint(-FOODDENSITY, FOODDENSITY)
    y = clusterY + random.randint(-FOODDENSITY, FOODDENSITY)
    foodSprite = Food.Food('sprites/plant.png', x, y)
    foodList.append(foodSprite)
    return foodList

if __name__ == "__main__":
    #set config file
    if (MODE == 0):
        configPath = './neat-config-predators.txt'
    elif (MODE == 1):
        configPath = './neat-config-herbivores.txt'
    else:
        configPath = './neat-config-predators.txt'

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    p = neat.Population(config)

    #data output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    
    if (MODE == 0):
        print('Training Predators...')
        #run neat
        winner = p.run(trainPredator, 500)
        #save winner
        with open("predator.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()
    elif (MODE == 1):
        print('Training Herbivores...')
        #run neat
        winner = p.run(trainHerbivore, 500)
        #save winner
        with open("herbivore.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()
    else:
        print('Running Simulation...')
        configPathHerbivore = './neat-config-herbivores.txt'
        configPathPredator = './neat-config-predators.txt'

        herbivoreConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathHerbivore)
        predatorConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathPredator)

        # load herbivore
        with open("herbivore.pkl", "rb") as f:
            herbivoreGenome = pickle.load(f)
            f.close()

        # load predator
        with open("predator.pkl", "rb") as f:
            predatorGenome = pickle.load(f)
            f.close()

        runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig)