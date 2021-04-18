import pygame

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load(image)
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)