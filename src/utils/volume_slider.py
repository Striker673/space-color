from typing import Optional

import pygame



class VolumeSlider:
    def __init__(self, x: int, y: int, width: int, height: int, initial_value: float = 0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.dragging = False
        self.color = (200, 200, 200)
        self.handle_color = (255, 255, 255)
        self.handle_radius = height // 2
        self.handle_rect = pygame.Rect(0, 0, self.handle_radius * 2, self.handle_radius * 2)
        self.update_handle_position()

    def update_handle_position(self):
        x_pos = self.rect.x + (self.rect.width - self.handle_radius * 2) * self.value
        self.handle_rect.x = x_pos
        self.handle_rect.centery = self.rect.centery

    def handle_event(self, event: pygame.event.Event) -> Optional[float]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x_pos = max(self.rect.left, min(event.pos[0], self.rect.right - self.handle_radius * 2))
            self.value = (x_pos - self.rect.x) / (self.rect.width - self.handle_radius * 2)
            self.value = max(0.0, min(1.0, self.value))
            self.update_handle_position()
            return self.value

        return None

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)

        filled_rect = pygame.Rect(self.rect.x, self.rect.y,self.handle_rect.centerx - self.rect.x, self.rect.height)
        pygame.draw.rect(surface, (150, 150, 150), filled_rect)

        pygame.draw.circle(surface, self.handle_color, self.handle_rect.center, self.handle_radius)