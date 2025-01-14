import pygame
from utils.constants import COLORS


class PlatformSprite:
    def __init__(self):
        self.sprite_cache = {}

    def load_sprite(self, color: str) -> pygame.Surface:
        if color in self.sprite_cache:
            return self.sprite_cache[color]

        try:
            sprite = pygame.image.load(f"../assets/images/platform_{color}.png").convert_alpha()
            temp_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            temp_surface.blit(sprite, (0, 0))
            self.sprite_cache[color] = temp_surface
            return temp_surface
        except (FileNotFoundError, pygame.error) as e:
            print(f"Platform sprite not found or error loading: platform_{color}.png - {str(e)}")
            return None


class Platform(pygame.sprite.Sprite):
    sprite_manager = PlatformSprite()
    BASE_WIDTH = 128
    BASE_HEIGHT = 32

    def __init__(self, x: int, y: int, width: int, height: int, color: str):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height

        self.collision_surface = pygame.Surface([width, height], pygame.SRCALPHA)
        self.collision_surface.fill(COLORS[color])

        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)

        self.glow_surface = None
        self.create_platform_visuals()

    def create_platform_visuals(self) :
        sprite = self.sprite_manager.load_sprite(self.color)

        if sprite is None:
            self.create_fallback_visuals()
            return

        try:
            scale_factor = self.height / self.BASE_HEIGHT
            base_section_width = int(self.BASE_WIDTH * scale_factor)

            temp_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            temp_surface.blit(sprite, (0, 0))

            scaled_section = pygame.transform.smoothscale(temp_surface, (base_section_width, self.height))

            x_position = 0
            while x_position < self.width:
                remaining_width = self.width - x_position
                if remaining_width >= base_section_width:
                    self.image.blit(scaled_section, (x_position, 0))
                    x_position += base_section_width
                else:
                    subsurface = scaled_section.subsurface((0, 0, remaining_width, self.height))
                    self.image.blit(subsurface, (x_position, 0))
                    break

            self.add_effects()
        except (ValueError, pygame.error) as e:
            print(f"Error creating platform visuals: {str(e)}")
            self.create_fallback_visuals()

    def create_fallback_visuals(self) :
        self.image.fill(COLORS[self.color])
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.width, self.height), 1)

    def add_effects(self) :
        pygame.draw.rect(self.image, (255, 255, 255, 100), (0, 0, self.width, self.height), 1)

        highlight = pygame.Surface((self.width, 2), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 50))
        self.image.blit(highlight, (0, 0))


class MovingPlatform(Platform):
    def __init__(self, x: int, y: int, width: int, height: int, color: str, move_x: int = 0, move_y: int = 0,
                 speed: float = 2):
        super().__init__(x, y, width, height, color)
        self.start_x = x
        self.start_y = y
        self.move_x = move_x
        self.move_y = move_y
        self.speed = speed
        self.movement = 0

    def update(self) :
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
