import pygame
import random
import Herbivore
import Predator
import MenuButton
import Food
import neat
import pickle

WORLDSIZE = 1000
FPS = 1000

SPAWNBORDER = 50

POPULATION = 10
FOODDENSITY = 20
FOODMULTIPLIER = 1
FOODRESPAWN = 5
FOODCLUMPSIZE = 5
HREPRODUCTIONTHRESHOLD = 10000
PREPRODUCTIONTHRESHOLD = 100000

PTRAINFOODCOUNT = 20
PTRAINGENERATIONS = 500
HTRAINGENERATIONS = 500
HTRAINFOODCOUNT = 20
HTRAINPREDATORCOUNT = 10
HTRAINPREDATORMOVE = False

pygame.init()

screen = pygame.display.set_mode((WORLDSIZE, WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

def menu():
    click = False
    buttons = pygame.sprite.Group()
    trainPredatorButton = MenuButton.MenuButton('sprites/train_predators.png', 200, 100)
    trainHerbivoreButton = MenuButton.MenuButton('sprites/train_herbivores.png', 200, 300)
    runPlanetButton = MenuButton.MenuButton('sprites/run_planet.png', 200, 500)
    buttons.add(trainPredatorButton, trainHerbivoreButton, runPlanetButton)
    
    while True:
        #Events
        mx, my = pygame.mouse.get_pos()
        if (trainPredatorButton.rect.collidepoint((mx, my))):
            if (click):
                configPath = './neat-config-predators.txt'
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
                p = neat.Population(config)

                #data output
                p.add_reporter(neat.StdOutReporter(True))
                stats = neat.StatisticsReporter()
                p.add_reporter(stats)
                
                print('Training Predators...')
                #run neat
                winner = p.run(trainPredator, PTRAINGENERATIONS)
                #save winner
                with open("predator.pkl", "wb") as f:
                    pickle.dump(winner, f)
                    f.close()
        if (trainHerbivoreButton.rect.collidepoint((mx, my))):
            if (click):
                configPath = './neat-config-herbivores.txt'
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

                p = neat.Population(config)

                #data output
                p.add_reporter(neat.StdOutReporter(True))
                stats = neat.StatisticsReporter()
                p.add_reporter(stats)
                print('Training Herbivores...')
                #run neat
                winner = p.run(trainHerbivore, HTRAINGENERATIONS)
                #save winner
                with open("herbivore.pkl", "wb") as f:
                    pickle.dump(winner, f)
                    f.close()
        if (runPlanetButton.rect.collidepoint((mx, my))):
            if (click):
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
        
        click = False
        for event in pygame.event.get():
            #closing window
            if (event.type == pygame.QUIT):
                pygame.quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    click = True
        
        #Draw
        screen.fill((245, 222, 179))
        buttons.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(FPS)
############################END Menu############################

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
    for i in range(PTRAINFOODCOUNT):
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

    allSprites = pygame.sprite.Group()
    
    if (HTRAINPREDATORMOVE):
        configPathPredator = './neat-config-predators.txt'
        predatorConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathPredator)
        # load predator genome
        with open("predator.pkl", "rb") as f:
            predatorGenome = pickle.load(f)
            f.close()
        #create predator brain
        predatorNet = neat.nn.FeedForwardNetwork.create(predatorGenome, predatorConfig)


    for i in range(HTRAINPREDATORCOUNT):
        x = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        y = random.randint(SPAWNBORDER, (WORLDSIZE - SPAWNBORDER))
        predator = Predator.Predator('sprites/creature_red.png', x, y, 1)
        predator.viewDistance = 1500
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
            
        herbivores.append(animat)
    
    foodList = []
    for i in range(HTRAINFOODCOUNT):
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
            if (HTRAINPREDATORMOVE):
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
        clock.tick(FPS)
############################END trainHerbivore############################

def runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig):
        
    #init NEAT
    herbivores = []
    predators = []

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
            if (herbivore.energy > HREPRODUCTIONTHRESHOLD):
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
            
            if (predator.energy > PREPRODUCTIONTHRESHOLD):
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
    menu()