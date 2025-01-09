import pygame
from ..utils.constants import COLORS

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: str):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(COLORS[color])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color