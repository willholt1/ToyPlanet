import pygame
import constants
class Food(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #200 for training
        self.energy = constants.FOODENERGY

    def getPosition(self):
       print('x = {} & y = {}'.format(self.center_x, self.center_y))