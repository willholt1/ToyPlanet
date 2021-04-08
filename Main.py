import pygame
import random
import Creature
import Food
import neat
import pickle

WORLDSIZE = 1000
FPS = 1000

SPAWNBORDER = 50

POPULATION = 100
FOODDENSITY = 30
FOODMULTIPLIER = 1
FOODRESPAWN = 5

GENOMEPATH = 'winner.pkl'
MODE = 1

def runPlanetTrain(genomes, config):
    
    #init NEAT
    nets = []
    herbivores = []

    pygame.init()

    screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
    pygame.display.set_caption('Toy Planet')
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()


    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        animat = Creature.Creature('sprites/creature_blue.png', x, y)
            
        herbivores.append(animat)

    foodList = []
    for i in range(POPULATION * FOODMULTIPLIER):
        foodList = replenishFood(foodList)

    ###########
    #Main loop#
    ###########
    running = True
    while running:
        #Events
        for event in pygame.event.get():
            #closing window
            if event.type == pygame.QUIT:
                pygame.quit()

        #Update
        allSprites.empty()
        aliveCreatues = 0
        for i, herbivore in enumerate(herbivores):
            output = nets[i].activate(herbivore.getData())
            decision = output.index(max(output)) + 1
            foodList = herbivore.update(foodList, decision)
            genomes[i][1].fitness = herbivore.fitness
            
            if (herbivore.alive):
                aliveCreatues += 1

        if (aliveCreatues == 0):
            running = False

        #chance more food is generated. if more creatures, greater chance for food to be generated
        #(random.randint(0,100) < (30 - round(len(herbivores)/4))) and (len(foodList) < 500)
        if (random.randint(0,100) < FOODRESPAWN):
            foodList = replenishFood(foodList)

        allSprites.add(herbivores, foodList)
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        
        #always flip last
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(FPS)

def replenishFood(foodList):
    clusterX = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    clusterY = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
    for i in range(random.randint(1, 3)):
        x = clusterX + random.randint(-FOODDENSITY, FOODDENSITY)
        y = clusterY + random.randint(-FOODDENSITY, FOODDENSITY)
        foodSprite = Food.Food('sprites/plant.png', x, y)
        foodList.append(foodSprite)
    return foodList

def runPlanet(genomes, config):
        
    #init NEAT
    herbivores = []

    pygame.init()

    screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
    pygame.display.set_caption('Toy Planet')
    clock = pygame.time.Clock()
    allSprites = pygame.sprite.Group()

    net = neat.nn.FeedForwardNetwork.create(genomes, config)

    for id in (range(POPULATION)):

        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        animat = Creature.Creature('sprites/creature_blue.png', x, y)
            
        herbivores.append(animat)

    foodList = []
    for i in range(POPULATION * FOODMULTIPLIER):
        foodList = replenishFood(foodList)

    ###########
    #Main loop#
    ###########
    running = True
    while running:
        #Events
        for event in pygame.event.get():
            #closing window
            if event.type == pygame.QUIT:
                pygame.quit()

        #Update
        allSprites.empty()
        aliveCreatues = 0
        for herbivore in herbivores:
            output = net.activate(herbivore.getData())
            decision = output.index(max(output)) + 1
            foodList = herbivore.update(foodList, decision)
            
            if (herbivore.alive):
                aliveCreatues += 1

        if (aliveCreatues == 0):
            running = False

        #chance more food is generated. if more creatures, greater chance for food to be generated
        #(random.randint(0,100) < (30 - round(len(herbivores)/4))) and (len(foodList) < 500)
        if (random.randint(0,100) < FOODRESPAWN):
            foodList = replenishFood(foodList)

        allSprites.add(herbivores, foodList)
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        
        #always flip last
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(FPS)


if __name__ == "__main__":
    #set config file
    configPath = './neat-config.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    p = neat.Population(config)

    #data output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    
    if (MODE == 0):
        #run neat
        winner = p.run(runPlanetTrain, 10)
        #save winner
        with open(GENOMEPATH, "wb") as f:
            pickle.dump(winner, f)
            f.close()
    else:
        # load winner
        with open(GENOMEPATH, "rb") as f:
            genomes = pickle.load(f)

        # Convert loaded genome into required data structure
        #genomes = [(1, genome)]

        runPlanet(genomes, config)