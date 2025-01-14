import pygame
from states.game_state import GameState
from level_generator import LevelGenerator
from sprites.player import Player
from sprites.platform import Platform
from utils.camera import Camera
from utils.constants import COLORS
from utils.shader import Shader
from utils.background import BackgroundManager

from src.utils.audio_manager import AudioManager


class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.player = None
        self.camera = Camera(game.screen.get_width(), game.screen.get_height())
        self.level_generator = LevelGenerator(game.screen.get_width() * 3, game.screen.get_height())

        self.background = BackgroundManager(game.screen.get_width(), game.screen.get_height())

        self.score = 0
        self.lives = 10
        self.font = pygame.font.Font(None, 36)
        self.audio_manager = AudioManager()

        self.init_level()

    def init_level(self) :
        self.all_sprites.empty()
        self.platforms.empty()
        self.collectibles.empty()
        self.borders.empty()
        self.background.change_background()
        if self.player:
            self.player.kill()
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        border_width = self.game.screen.get_width() * 6
        border_height = self.game.screen.get_height() + 400

        top_border = Platform(0, -200, border_width, 1, "white")
        bottom_border = Platform(-200, self.game.screen.get_height() + 200, border_width, 1, "white")
        left_border = Platform(-200, -200, 1, border_height, "white")
        right_border = Platform(border_width - 200, -200, 1, border_height, "white")

        self.borders.add(top_border, bottom_border, left_border, right_border)

        platforms, collectibles = self.level_generator.generate_platforms(20)

        for platform in platforms:
            self.platforms.add(platform)
            self.all_sprites.add(platform)

        for collectible in collectibles:
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)

    def handle_event(self, event: pygame.event.Event) :
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player.can_jump:
                self.player.jump()
                self.audio_manager.play_sound('jump')
            elif event.key == pygame.K_q:
                self.player.change_color("red")
            elif event.key == pygame.K_w:
                self.player.change_color("blue")
            elif event.key == pygame.K_e:
                self.player.change_color("yellow")
            elif event.key == pygame.K_p:
                self.game.change_state('pause')
            elif event.key == pygame.K_r:
                self.reset_game()

    def update(self) :
        self.all_sprites.update()
        self.handle_collisions()
        self.camera.update(self.player)
        self.background.update()

    def handle_collisions(self) :
        if pygame.sprite.spritecollideany(self.player, self.borders):
            self.handle_death()
            return

        on_ground = False
        platforms_hit = pygame.sprite.spritecollide(self.player, self.platforms, False)

        for platform in platforms_hit:
            if self.player.current_color == platform.color:
                if self.player.velocity_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.can_jump = True
                    self.player.is_jumping = False
                    on_ground = True
                elif self.player.velocity_y < 0:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0
            else:
                self.handle_death()
                return

        if not on_ground and self.player.velocity_y > 0:
            self.player.can_jump = False
            self.player.is_jumping = True

        collectibles_hit = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for collectible in collectibles_hit:
            self.audio_manager.play_sound('collect')
            if hasattr(collectible, 'is_level_end'):
                self.score += 10
                self.background.change_background()
                self.init_level()
            else:
                self.score += 1
                self.player.change_color(collectible.color)

    def handle_death(self) :
        self.audio_manager.play_sound('death')
        self.player.rect.x = 100
        self.player.rect.y = 100
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.change_color("red")

        self.lives -= 1
        if self.lives <= 0:
            if hasattr(self.game.states['menu'], 'final_score'):
                self.game.states['menu'].final_score = self.score
            self.game.change_state('menu')

    def reset_game(self) :
        self.background.change_background()
        self.lives = 10
        self.score = 0
        self.init_level()

    def render(self, screen: pygame.Surface) :
        self.background.draw(screen, self.camera.camera.x)

        for sprite in self.all_sprites:
            if isinstance(sprite, (Player, Platform)) and hasattr(sprite, 'color') and sprite.color != "white":
                Shader.apply_glow(sprite)
                glow_rect = sprite.glow_surface.get_rect(center=sprite.rect.center)
                screen.blit(sprite.glow_surface, self.camera.apply_rect(glow_rect))

        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))

        score_text = self.font.render(f'Score: {self.score}', True, COLORS["white"])
        lives_text = self.font.render(f'Lives: {self.lives}', True, COLORS["white"])
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
