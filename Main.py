#############################################################
#entry point for the program and contains the menu game loop#
#############################################################
#libraries
import pygame
import neat
import pickle
#classes
import MenuButton
#misc
import constants
import runPlanet
import trainHerbivore
import trainPredator

#setup pygame window
pygame.init()
screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
pygame.display.set_caption('Toy Planet')
clock = pygame.time.Clock()

#declare fonts
font = pygame.font.SysFont('timesnewroman', 36)
labelFont = pygame.font.SysFont('timesnewroman', 24)

def menu():
    click = False
    #create all the button objects and add to sprite group to display
    buttons = pygame.sprite.Group()
    trainPredatorButton = MenuButton.MenuButton('sprites/train_predators.png', 170, 100)
    trainHerbivoreButton = MenuButton.MenuButton('sprites/train_herbivores.png', 170, 300)
    runPlanetButton = MenuButton.MenuButton('sprites/run_planet.png', 170, 600)
    
    pTrainFoodCountPlus = MenuButton.MenuButton('sprites/plus_button.png', 500, 100)
    pTrainFoodCountMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 100)
    
    pTrainGenerationsPlus = MenuButton.MenuButton('sprites/plus_button.png', 825, 100)
    pTrainGenerationsMinus = MenuButton.MenuButton('sprites/minus_button.png', 700, 100)
    
    hTrainFoodCountPlus = MenuButton.MenuButton('sprites/plus_button.png', 500, 300)
    hTrainFoodCountMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 300)
    
    hTrainGenerationsPlus = MenuButton.MenuButton('sprites/plus_button.png', 825, 300)
    hTrainGenerationsMinus = MenuButton.MenuButton('sprites/minus_button.png', 700, 300)
    
    hTrainPredatorCountPlus = MenuButton.MenuButton('sprites/plus_button.png', 500, 450)
    hTrainPredatorCountMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 450)
    
    hTrainPredatorMoveToggle = MenuButton.MenuButton('sprites/toggle_button.png', 715, 450)
    
    populationPlus = MenuButton.MenuButton('sprites/plus_button.png', 500, 600)
    populationMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 600)
    
    foodRespawnPlus = MenuButton.MenuButton('sprites/plus_button.png', 800, 600)
    foodRespawnMinus = MenuButton.MenuButton('sprites/minus_button.png', 700, 600)
    
    foodDensityPlus = MenuButton.MenuButton('sprites/plus_button.png', 500, 750)
    foodDensityMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 750)

    foodClumpSizePlus = MenuButton.MenuButton('sprites/plus_button.png', 800, 750)
    foodClumpSizeMinus = MenuButton.MenuButton('sprites/minus_button.png', 700, 750)

    hReproPlus = MenuButton.MenuButton('sprites/plus_button.png', 575, 900)
    hReproMinus = MenuButton.MenuButton('sprites/minus_button.png', 400, 900)

    pReproPlus = MenuButton.MenuButton('sprites/plus_button.png', 875, 900)
    pReproMinus = MenuButton.MenuButton('sprites/minus_button.png', 700, 900)

    fpsPlus = MenuButton.MenuButton('sprites/plus_button.png', 225, 750)
    fpsMinus = MenuButton.MenuButton('sprites/minus_button.png', 100, 750)

    foodEnergyPlus = MenuButton.MenuButton('sprites/plus_button.png', 225, 900)
    foodEnergyMinus = MenuButton.MenuButton('sprites/minus_button.png', 100, 900)

    buttons.add(trainPredatorButton,
                trainHerbivoreButton,
                runPlanetButton,
                pTrainFoodCountPlus,
                pTrainFoodCountMinus,
                pTrainGenerationsPlus,
                pTrainGenerationsMinus,
                hTrainFoodCountPlus,
                hTrainFoodCountMinus,
                hTrainGenerationsPlus,
                hTrainGenerationsMinus,
                hTrainPredatorCountPlus,
                hTrainPredatorCountMinus,
                hTrainPredatorMoveToggle,
                populationPlus,
                populationMinus,
                foodRespawnPlus,
                foodRespawnMinus,
                foodDensityPlus,
                foodDensityMinus,
                foodClumpSizePlus,
                foodClumpSizeMinus,
                hReproPlus,
                hReproMinus,
                pReproPlus,
                pReproMinus,
                fpsPlus,
                fpsMinus,
                foodEnergyPlus,
                foodEnergyMinus)
    
    #menu game loop
    while True:
        #Events
        #if the mouse position is over a button and the mouse is clicked then do the corresponding action
        mx, my = pygame.mouse.get_pos()
        if (pTrainFoodCountPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PTRAINFOODCOUNT < 99):
                    constants.PTRAINFOODCOUNT += 1
        if (pTrainFoodCountMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PTRAINFOODCOUNT > 1):
                    constants.PTRAINFOODCOUNT -= 1
        if (pTrainGenerationsPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PTRAINGENERATIONS < 990):
                    constants.PTRAINGENERATIONS += 10
        if (pTrainGenerationsMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PTRAINGENERATIONS > 10):
                    constants.PTRAINGENERATIONS -= 10
        if (hTrainFoodCountPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINFOODCOUNT < 99):
                    constants.HTRAINFOODCOUNT += 1
        if (hTrainFoodCountMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINFOODCOUNT > 1):
                    constants.HTRAINFOODCOUNT -= 1
        if (hTrainGenerationsPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINGENERATIONS < 990):
                    constants.HTRAINGENERATIONS += 10
        if (hTrainGenerationsMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINGENERATIONS > 10):
                    constants.HTRAINGENERATIONS -= 10
        if (hTrainPredatorCountPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINPREDATORCOUNT < 99):
                    constants.HTRAINPREDATORCOUNT += 1
        if (hTrainPredatorCountMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINPREDATORCOUNT > 1):
                    constants.HTRAINPREDATORCOUNT -= 1
        if (hTrainPredatorMoveToggle.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HTRAINPREDATORMOVE == True):
                    constants.HTRAINPREDATORMOVE = False
                else:
                    constants.HTRAINPREDATORMOVE = True
        if (populationPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.POPULATION < 99):
                    constants.POPULATION += 1
        if (populationMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.POPULATION > 1):
                    constants.POPULATION -= 1
        if (foodRespawnPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODRESPAWN < 50):
                    constants.FOODRESPAWN += 1
        if (foodRespawnMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODRESPAWN > 1):
                    constants.FOODRESPAWN -= 1
        if (foodDensityPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODDENSITY < 40):
                    constants.FOODDENSITY += 1
        if (foodDensityMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODDENSITY > 1):
                    constants.FOODDENSITY -= 1
        if (foodClumpSizePlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODCLUMPSIZE < 20):
                    constants.FOODCLUMPSIZE += 1
        if (foodClumpSizeMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODCLUMPSIZE > 1):
                    constants.FOODCLUMPSIZE -= 1
        if (hReproPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HREPRODUCTIONTHRESHOLD < 999500):
                    constants.HREPRODUCTIONTHRESHOLD += 500
        if (hReproMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.HREPRODUCTIONTHRESHOLD > 500):
                    constants.HREPRODUCTIONTHRESHOLD -= 500
        if (pReproPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PREPRODUCTIONTHRESHOLD < 999500):
                    constants.PREPRODUCTIONTHRESHOLD += 500
        if (pReproMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.PREPRODUCTIONTHRESHOLD > 500):
                    constants.PREPRODUCTIONTHRESHOLD -= 500
        if (fpsPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FPS < 990):
                    constants.FPS += 10
        if (fpsMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FPS > 10):
                    constants.FPS -= 10
        if (foodEnergyPlus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODENERGY < 990):
                    constants.FOODENERGY += 10
        if (foodEnergyMinus.rect.collidepoint((mx, my))):
            if (click):
                if (constants.FOODENERGY > 10):
                    constants.FOODENERGY -= 10
        if (trainPredatorButton.rect.collidepoint((mx, my))):
            if (click):
                print('Training Predators...\npress esc to skip generation')
                #load neat config
                configPath = 'NEAT_configs/neat-config-predators.txt'
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
                p = neat.Population(config)

                #data output
                p.add_reporter(neat.StdOutReporter(True))
                stats = neat.StatisticsReporter()
                p.add_reporter(stats)
                
                #run neat
                winner = p.run(trainPredator.trainPredator, constants.PTRAINGENERATIONS)
                #save winner
                with open("savedNNs/predator.pkl", "wb") as f:
                    pickle.dump(winner, f)
                    f.close()
        if (trainHerbivoreButton.rect.collidepoint((mx, my))):
            if (click):
                print('Training Herbivores...\npress esc to skip generation')
                #load neat config
                configPath = 'NEAT_configs/neat-config-herbivores.txt'
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
                p = neat.Population(config)

                #data output
                p.add_reporter(neat.StdOutReporter(True))
                stats = neat.StatisticsReporter()
                p.add_reporter(stats)

                #run neat
                winner = p.run(trainHerbivore.trainHerbivore, constants.HTRAINGENERATIONS)
                #save winner
                with open("savedNNs/herbivore.pkl", "wb") as f:
                    pickle.dump(winner, f)
                    f.close()
        if (runPlanetButton.rect.collidepoint((mx, my))):
            if (click):
                print('Running Simulation...\npress esc to terminate')
                #load neat configs
                configPathHerbivore = 'NEAT_configs/neat-config-herbivores.txt'
                configPathPredator = 'NEAT_configs/neat-config-predators.txt'
                herbivoreConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathHerbivore)
                predatorConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPathPredator)

                # load herbivore NN
                with open("savedNNs/herbivore.pkl", "rb") as f:
                    herbivoreGenome = pickle.load(f)
                    f.close()

                # load predator NN
                with open("savedNNs/predator.pkl", "rb") as f:
                    predatorGenome = pickle.load(f)
                    f.close()

                runPlanet.runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig)
        
        click = False
        for event in pygame.event.get():
            #closing window
            if (event.type == pygame.QUIT):
                pygame.quit()
            #if click
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    click = True
        
        #Draw
        screen.fill((245, 222, 179))
        buttons.draw(screen)
        #draw labels and values for the menu
        #pTrainFoodCount
        img = font.render(str(constants.PTRAINFOODCOUNT), True, (0,0,0))
        screen.blit(img, (432, 80))
        img = labelFont.render('Ammount of food:', True, (0,0,0))
        screen.blit(img, (370, 40))
        #pTrainGenerations
        img = font.render(str(constants.PTRAINGENERATIONS), True, (0,0,0))
        screen.blit(img, (735, 80))
        img = labelFont.render('Generations:', True, (0,0,0))
        screen.blit(img, (700, 40))
        #hTrainFoodCount
        img = font.render(str(constants.HTRAINFOODCOUNT), True, (0,0,0))
        screen.blit(img, (432, 280))
        img = labelFont.render('Ammount of food:', True, (0,0,0))
        screen.blit(img, (370, 240))
        #hTrainGenerations
        img = font.render(str(constants.HTRAINGENERATIONS), True, (0,0,0))
        screen.blit(img, (735, 280))
        img = labelFont.render('Generations:', True, (0,0,0))
        screen.blit(img, (700, 240))
        #hTrainPredatorCount
        img = font.render(str(constants.HTRAINPREDATORCOUNT), True, (0,0,0))
        screen.blit(img, (432, 430))
        img = labelFont.render('Number of Predators:', True, (0,0,0))
        screen.blit(img, (360, 390))
        #hTrainPredatorMove
        img = font.render(str(constants.HTRAINPREDATORMOVE), True, (0,0,0))
        screen.blit(img, (785, 430))
        img = labelFont.render('Moving Predators:', True, (0,0,0))
        screen.blit(img, (675, 390))
        #population
        img = font.render(str(constants.POPULATION), True, (0,0,0))
        screen.blit(img, (432, 580))
        img = labelFont.render('Population:', True, (0,0,0))
        screen.blit(img, (390, 540))
        #foodRespawn
        img = font.render(str(constants.FOODRESPAWN), True, (0,0,0))
        screen.blit(img, (732, 580))
        img = labelFont.render('Food respawn rate:', True, (0,0,0))
        screen.blit(img, (670, 540))
        #foodDensity
        img = font.render(str(constants.FOODDENSITY), True, (0,0,0))
        screen.blit(img, (432, 730))
        img = labelFont.render('Food clump spacing:', True, (0,0,0))
        screen.blit(img, (360, 690))
        #foodClumpSize
        img = font.render(str(constants.FOODCLUMPSIZE), True, (0,0,0))
        screen.blit(img, (732, 730))
        img = labelFont.render('Max food per clump:', True, (0,0,0))
        screen.blit(img, (660, 690))
        #hReproductionThreshold
        img = font.render(str(constants.HREPRODUCTIONTHRESHOLD), True, (0,0,0))
        screen.blit(img, (432, 880))
        img = labelFont.render('Herbivore reproduction', True, (0,0,0))
        screen.blit(img, (360, 815))
        img = labelFont.render('threshold:', True, (0,0,0))
        screen.blit(img, (360, 840))
        #pReproductionThreshold
        img = font.render(str(constants.PREPRODUCTIONTHRESHOLD), True, (0,0,0))
        screen.blit(img, (732, 880))
        img = labelFont.render('Predator reproduction', True, (0,0,0))
        screen.blit(img, (660, 815))
        img = labelFont.render('threshold:', True, (0,0,0))
        screen.blit(img, (660, 840))
        #fps
        img = font.render(str(constants.FPS), True, (0,0,0))
        screen.blit(img, (132, 730))
        img = labelFont.render('FPS:', True, (0,0,0))
        screen.blit(img, (132, 690))
        #food Energy
        img = font.render(str(constants.FOODENERGY), True, (0,0,0))
        screen.blit(img, (132, 880))
        img = labelFont.render('Food energy:', True, (0,0,0))
        screen.blit(img, (105, 840))
        #draw borders
        pygame.draw.line(screen, (0,0,0), (0, 175), (1000, 175), 3)
        pygame.draw.line(screen, (0,0,0), (0, 525), (1000, 525), 3)
        pygame.draw.line(screen, (0,0,0), (0, 675), (300, 675), 3)
        pygame.draw.line(screen, (0,0,0), (300, 1000), (300, 675), 3)

        pygame.display.flip()
        #keep program running at set FPS
        clock.tick(constants.FPS)
############################END Menu############################

if __name__ == "__main__":
    menu()