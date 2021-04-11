import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.energy = 200

    def getPosition(self):
       print('x = {} & y = {}'.format(self.center_x, self.center_y))