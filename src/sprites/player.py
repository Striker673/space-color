import pygame
from utils.constants import COLORS


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.size = 40
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 7.5
        self.jump_power = -20.5
        self.gravity = 0.8
        self.can_jump = True
        self.is_jumping = False

        self.current_color = "red"
        self.color = COLORS["red"]
        self.glow_surface = None
        self.glow_rect = None
        self.update_appearance()

    def update_appearance(self):
        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), border_radius=5)

        highlight = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(highlight, (255, 255, 255, 50), (2, 2, self.size - 4, self.size // 3), border_radius=3)
        self.image.blit(highlight, (0, 0))

    def update(self) -> None:
        self.apply_gravity()
        self.handle_movement()
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def handle_movement(self) -> None:
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

        self.is_jumping = not self.can_jump

    def change_color(self, color_name: str) -> None:
        if color_name in COLORS and color_name != self.current_color:
            self.color = COLORS[color_name]
            self.current_color = color_name
            self.update_appearance()
    def apply_gravity(self) -> None:
        self.velocity_y += self.gravity

    def jump(self) -> None:
        if self.can_jump:
            self.velocity_y = self.jump_power
            self.can_jump = False
            self.is_jumping = True
