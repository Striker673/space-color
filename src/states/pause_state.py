import pygame
from states.game_state import GameState
from utils.constants import COLORS
from utils.volume_slider import VolumeSlider
from utils.audio_manager import AudioManager


class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.audio_manager = AudioManager()

        self.resume_text = self.font.render('Resume (R)', True, COLORS["white"])
        self.quit_text = self.font.render('Quit to Menu (Q)', True, COLORS["white"])

        slider_width = 200
        slider_height = 20
        self.music_slider = VolumeSlider(game.screen.get_width() // 2 - slider_width // 2, 400, slider_width,
            slider_height, self.audio_manager.music_volume)
        self.sfx_slider = VolumeSlider(game.screen.get_width() // 2 - slider_width // 2, 470, slider_width,
            slider_height, self.audio_manager.sfx_volume)

    def handle_event(self, event: pygame.event.Event) :
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.audio_manager.play_sound('collect')
                self.game.change_state('play')
            elif event.key == pygame.K_q:
                self.game.change_state('menu')

        music_value = self.music_slider.handle_event(event)
        sfx_value = self.sfx_slider.handle_event(event)

        if music_value is not None:
            self.audio_manager.set_music_volume(music_value)
        if sfx_value is not None:
            self.audio_manager.set_sfx_volume(sfx_value)

    def render(self, screen: pygame.Surface) :
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        resume_rect = self.resume_text.get_rect(center=(screen.get_width() // 2, 200))
        quit_rect = self.quit_text.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(self.resume_text, resume_rect)
        screen.blit(self.quit_text, quit_rect)

        music_text = self.small_font.render('Music Volume:', True, COLORS["white"])
        sfx_text = self.small_font.render('SFX Volume:', True, COLORS["white"])
        screen.blit(music_text, (self.music_slider.rect.x, self.music_slider.rect.y - 25))
        screen.blit(sfx_text, (self.sfx_slider.rect.x, self.sfx_slider.rect.y - 25))

        self.music_slider.draw(screen)
        self.sfx_slider.draw(screen)
