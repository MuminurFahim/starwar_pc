import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.sr = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/predator.jpg')
        self.image = pygame.transform.scale(self.image, (76.5, 113.4))
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def update(self):
        # self.x += self.ai_settings.direction * self.ai_settings.alien_speed_factor
        # self.rect.x = self.x
        self.rect.x += self.ai_settings.direction * self.ai_settings.alien_speed_factor
        # print(str(self.ai_settings.direction) + '\t' + str(self.rect.x))
