import pygame

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass