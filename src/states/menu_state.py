import pygame
from states.game_state import GameState
from utils.constants import COLORS
from utils.audio_manager import AudioManager
from utils.background import BackgroundManager
from utils.volume_slider import VolumeSlider


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.audio_manager = AudioManager()
        self.audio_manager.play_music()

        self.title = self.font.render('Space Color', True, COLORS["white"])
        self.start_text = self.font.render('Press SPACE to Start', True, COLORS["white"])
        self.quit_text = self.font.render('Press Q to Quit', True, COLORS["white"])

        self.background = BackgroundManager(game.screen.get_width(), game.screen.get_height())

        self.final_score = 0
        self.high_score = 0

        slider_width = 200
        slider_height = 20
        self.music_slider = VolumeSlider(game.screen.get_width() // 2 - slider_width // 2, 500, slider_width,
            slider_height, self.audio_manager.music_volume)
        self.sfx_slider = VolumeSlider(game.screen.get_width() // 2 - slider_width // 2, 570, slider_width,
            slider_height, self.audio_manager.sfx_volume)

    def handle_event(self, event: pygame.event.Event) :
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.audio_manager.play_sound('collect')
                play_state = self.game.states['play']
                play_state.reset_game()
                self.game.change_state('play')
                self.final_score = 0
            elif event.key == pygame.K_q:
                self.game.running = False

        music_value = self.music_slider.handle_event(event)
        sfx_value = self.sfx_slider.handle_event(event)

        if music_value is not None:
            self.audio_manager.set_music_volume(music_value)
        if sfx_value is not None:
            self.audio_manager.set_sfx_volume(sfx_value)

    def update(self) :
        self.background.update()
        if self.final_score > self.high_score:
            self.high_score = self.final_score

    def render(self, screen: pygame.Surface) :
        self.background.draw(screen)

        screen.blit(self.title, self.title.get_rect(center=(screen.get_width() // 2, 150)))
        screen.blit(self.start_text, self.start_text.get_rect(center=(screen.get_width() // 2, 250)))
        screen.blit(self.quit_text, self.quit_text.get_rect(center=(screen.get_width() // 2, 350)))

        if self.final_score > 0:
            score_text = self.small_font.render(f'Final Score: {self.final_score}', True, COLORS["white"])
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, 420))
            screen.blit(score_text, score_rect)

        if self.high_score > 0:
            high_score_text = self.small_font.render(f'High Score: {self.high_score}', True, COLORS["white"])
            high_score_rect = high_score_text.get_rect(center=(screen.get_width() // 2, 460))
            screen.blit(high_score_text, high_score_rect)

        music_text = self.small_font.render('Music Volume:', True, COLORS["white"])
        sfx_text = self.small_font.render('SFX Volume:', True, COLORS["white"])
        screen.blit(music_text, (self.music_slider.rect.x, self.music_slider.rect.y - 25))
        screen.blit(sfx_text, (self.sfx_slider.rect.x, self.sfx_slider.rect.y - 25))

        self.music_slider.draw(screen)
        self.sfx_slider.draw(screen)

        controls_text = self.small_font.render('Controls: Arrow Keys to Move, Space to Jump', True, COLORS["white"])
        colors_text = self.small_font.render('Q: Red, W: Blue, E: Yellow, R: Restart', True, COLORS["white"])
        screen.blit(controls_text, controls_text.get_rect(center=(screen.get_width() // 2, 650)))
        screen.blit(colors_text, colors_text.get_rect(center=(screen.get_width() // 2, 680)))
