##################################
#game loop for training predators#
##################################
#libraries
import pygame
import neat
#classes
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

def trainPredator(genomes, config):
    #init NEAT
    nets = []
    predators = []
    constants.HTRAINPREDATORMOVE = True
    allSprites = pygame.sprite.Group()

    #create predators
    for id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        x = 500
        y = 500
        predator = Predator.Predator('sprites/creature_red.png', x, y)
        predator.training = True
        predator.sleepTime = 1
        predators.append(predator)
    
    #create food
    foodList = []
    for i in range(constants.PTRAINFOODCOUNT):
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

        #Update predators
        allSprites.empty()
        aliveCreatues = 0
        for i, predator in enumerate(predators):  
            if (predator.alive):
                #pass data through NN
                output = nets[i].activate(predator.getData())
                #pass output of NN to the predator update function
                decision = output.index(max(output)) + 1
                foodList = predator.update(foodList, decision)
                genomes[i][1].fitness = predator.fitness
                aliveCreatues += 1

                #generate more food if any was eaten
                if (len(foodList)< lastFoodLen):
                    foodList = utility.trainReplenishFood(foodList)

                lastFoodLen = len(foodList)

        if (aliveCreatues == 0):
            running = False

        allSprites.add(predators, foodList)
        
        #Draw
        screen.fill((245, 222, 179))
        allSprites.draw(screen)
        pygame.display.flip()

        #keep program running at set FPS
        clock.tick(constants.FPS)

