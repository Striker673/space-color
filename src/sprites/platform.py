import pygame
from utils.constants import COLORS


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: str):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.glow_surface = None
        self.glow_rect = None
        self.update_appearance()

    def update_appearance(self):
        pygame.draw.rect(self.image, COLORS[self.color],(0, 0, self.rect.width, self.rect.height),border_radius=3)

        # Add subtle top highlight
        highlight = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(highlight, (255, 255, 255, 30),(0, 0, self.rect.width, self.rect.height // 3),border_radius=2)
        self.image.blit(highlight, (0, 0))


class MovingPlatform(Platform):
    def __init__(self, x: int, y: int, width: int, height: int, color: str,move_x: int = 0, move_y: int = 0, speed: float = 2):
        super().__init__(x, y, width, height, color)
        self.start_x = x
        self.start_y = y
        self.move_x = move_x
        self.move_y = move_y
        self.speed = speed
        self.movement = 0

    def update(self) -> None:
        if self.move_x:
            self.rect.x = self.start_x + self.movement
            if abs(self.movement) > abs(self.move_x):
                self.speed = -self.speed
            self.movement += self.speed

        if self.move_y:
            self.rect.y = self.start_y + self.movement
            if abs(self.movement) > abs(self.move_y):
                self.speed = -self.speed
            self.movement += self.speed
