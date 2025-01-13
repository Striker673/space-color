import pygame

from src.utils.constants import COLORS


class GlowEffect:
    @staticmethod
    def create_glow_surface(original_surface: pygame.Surface, glow_color: tuple, glow_size: int = 40) -> pygame.Surface:
        width = original_surface.get_width() + glow_size * 2
        height = original_surface.get_height() + glow_size * 2
        glow = pygame.Surface((width, height), pygame.SRCALPHA)

        for i in range(3):
            size = original_surface.get_size()
            scaled = pygame.transform.scale(original_surface,
                                            (size[0] + (i * 4), size[1] + (i * 4)))
            scaled.set_alpha(150 - i * 30)

            color_surface = pygame.Surface(scaled.get_size(), pygame.SRCALPHA)
            color_surface.fill((*glow_color[:3], 150))

            color_surface.blit(scaled, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            x = glow_size - i * 2
            y = glow_size - i * 2
            glow.blit(color_surface, (x, y))

        return glow


class Shader:
    @staticmethod
    def apply_glow(sprite: pygame.sprite.Sprite) -> None:
        if hasattr(sprite, 'color'):
            color = sprite.color if isinstance(sprite.color, tuple) else COLORS[sprite.color]
        else:
            color = sprite.image.get_at((0, 0))

        sprite.glow_surface = GlowEffect.create_glow_surface(sprite.image, color)
        sprite.glow_rect = sprite.glow_surface.get_rect()
        sprite.glow_rect.center = sprite.rect.center
