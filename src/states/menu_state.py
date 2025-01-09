import pygame
from .game_state import GameState
from ..utils.constants import COLORS


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Space Color', True, COLORS["white"])
        self.start_text = self.font.render('Press SPACE to Start', True, COLORS["white"])
        self.quit_text = self.font.render('Press Q to Quit', True, COLORS["white"])

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state('play')
            elif event.key == pygame.K_q:
                self.game.running = False

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(COLORS["black"])

        title_rect = self.title.get_rect(center=(screen.get_width() // 2, 200))
        start_rect = self.start_text.get_rect(center=(screen.get_width() // 2, 300))
        quit_rect = self.quit_text.get_rect(center=(screen.get_width() // 2, 400))

        screen.blit(self.title, title_rect)
        screen.blit(self.start_text, start_rect)
        screen.blit(self.quit_text, quit_rect)