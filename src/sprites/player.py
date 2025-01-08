import pygame
from ..utils.constants import COLORS


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = COLORS["red"]
        self.image.fill(self.color)

        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8

    def update(self) -> None:
        self.apply_gravity()
        self.handle_movement()
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def apply_gravity(self) -> None:
        self.velocity_y += self.gravity

    def handle_movement(self) -> None:
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

    def jump(self) -> None:
        self.velocity_y = self.jump_power

    def change_color(self, color_name: str) -> None:
        if color_name in COLORS:
            self.color = COLORS[color_name]
            self.image.fill(self.color)