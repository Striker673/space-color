import pygame
from states.game_state import GameState
from utils.constants import COLORS


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.title = self.font.render('Space Color', True, COLORS["white"])
        self.start_text = self.font.render('Press SPACE to Start', True, COLORS["white"])
        self.quit_text = self.font.render('Press Q to Quit', True, COLORS["white"])

        self.final_score = 0
        self.high_score = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_state = self.game.states['play']
                play_state.reset_game()
                self.game.change_state('play')
                self.final_score = 0
            elif event.key == pygame.K_q:
                self.game.running = False

    def update(self) -> None:
        if self.final_score > self.high_score:
            self.high_score = self.final_score

    def render(self, screen: pygame.Surface) -> None:
        screen.fill((20, 20, 40))

        screen.blit(self.title, self.title.get_rect(center=(screen.get_width() // 2, 150)))
        screen.blit(self.start_text, self.start_text.get_rect(center=(screen.get_width() // 2, 250)))
        screen.blit(self.quit_text, self.quit_text.get_rect(center=(screen.get_width() // 2, 350)))

        if self.final_score > 0:
            score_text = self.small_font.render(f'Final Score: {self.final_score}', True, COLORS["white"])
            screen.blit(score_text, score_text.get_rect(center=(screen.get_width() // 2, 420)))

        if self.high_score > 0:
            high_score_text = self.small_font.render(f'High Score: {self.high_score}', True, COLORS["white"])
            screen.blit(high_score_text, high_score_text.get_rect(center=(screen.get_width() // 2, 460)))

        controls_text = self.small_font.render('Controls: Arrow Keys to Move, Space to Jump', True, COLORS["white"])
        colors_text = self.small_font.render('Q: Red, W: Blue, E: Yellow, R: Restart', True, COLORS["white"])
        screen.blit(controls_text, controls_text.get_rect(center=(screen.get_width() // 2, 550)))
        screen.blit(colors_text, colors_text.get_rect(center=(screen.get_width() // 2, 590)))
