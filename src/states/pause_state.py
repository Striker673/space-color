import pygame
from states.game_state import GameState
from utils.constants import COLORS


class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.resume_text = self.font.render('Resume (R)', True, COLORS["white"])
        self.quit_text = self.font.render('Quit to Menu (Q)', True, COLORS["white"])

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.change_state('play')
            elif event.key == pygame.K_q:
                self.game.change_state('menu')

    def render(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        resume_rect = self.resume_text.get_rect(center=(screen.get_width() // 2, 200))
        quit_rect = self.quit_text.get_rect(center=(screen.get_width() // 2, 300))

        screen.blit(self.resume_text, resume_rect)
        screen.blit(self.quit_text, quit_rect)