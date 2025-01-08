import pygame
from typing import Dict, Optional
from .states.game_state import GameState


class Game:
    def __init__(self, width: int = 1280, height: int = 720):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Color Switcher")
        self.clock = pygame.time.Clock()
        self.running = True
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None

        self.init_states()

    def init_states(self) -> None:
        self.current_state = self.states['menu']

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.current_state:
                self.current_state.handle_event(event)

    def update(self) -> None:
        if self.current_state:
            self.current_state.update()

    def render(self) -> None:
        if self.current_state:
            self.current_state.render(self.screen)
        pygame.display.flip()

    def change_state(self, state_name: str) -> None:
        if state_name in self.states:
            self.current_state = self.states[state_name]