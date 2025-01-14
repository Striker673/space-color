import pygame
from typing import Dict, Optional
from states.pause_state import PauseState
from states.play_state import PlayState
from states.game_state import GameState
from states.menu_state import MenuState


class Game:
    def __init__(self, width: int = 1280, height: int = 720):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space Color")
        self.clock = pygame.time.Clock()
        self.running = True
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None
        self.init_states()

    def init_states(self) :
        self.states['menu'] = MenuState(self)
        self.states['play'] = PlayState(self)
        self.states['pause'] = PauseState(self)
        self.current_state = self.states['menu']

    def run(self) :
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.current_state:
                self.current_state.handle_event(event)

    def update(self) :
        if self.current_state:
            self.current_state.update()

    def render(self) :
        if self.current_state:
            self.current_state.render(self.screen)
        pygame.display.flip()

    def change_state(self, state_name: str) :
        if state_name in self.states:
            if state_name == 'menu' and isinstance(self.current_state, PlayState):
                self.states['menu'].final_score = self.current_state.score
            self.current_state = self.states[state_name]
