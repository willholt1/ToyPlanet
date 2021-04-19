import pygame
import random
import Herbivore
import Predator
import constants
import MenuButton
import Food
import neat
import pickle
import runPlanet
import trainHerbivore
import trainPredator

pygame.init()

screen = pygame.display.set_mode((constants.WORLDSIZE, constants.WORLDSIZE))
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
                winner = p.run(trainPredator.trainPredator, constants.PTRAINGENERATIONS)
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
                winner = p.run(trainHerbivore.trainHerbivore, constants.HTRAINGENERATIONS)
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

                runPlanet.runPlanet(herbivoreGenome, predatorGenome, herbivoreConfig, predatorConfig)
        
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
        clock.tick(constants.FPS)
############################END Menu############################


if __name__ == "__main__":
    menu()