########################
# class for food sprite#
########################
#libraries
import pygame
#misc
import constants
class Food(pygame.sprite.Sprite):
    def __init__(self, image, x, y):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.energy = constants.FOODENERGY