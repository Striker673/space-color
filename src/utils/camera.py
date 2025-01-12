import pygame

class Camera:
    def __init__(self, width: int, height: int):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        return entity.rect.move(self.camera.topleft)

    def update(self, target) -> None:
        x = -target.rect.centerx + self.width // 2
        y = -target.rect.centery + self.height // 2

        x = min(400, x)
        y = min(300, y)
        x = max(-(self.width * 3 + 400), x)
        y = max(-(self.height + 300), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
