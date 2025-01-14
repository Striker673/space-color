import pygame
from utils.constants import COLORS

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: str):
        super().__init__()
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(COLORS[color])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

class LevelEndOrb(Collectible):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "white")
        self.is_level_end = True
