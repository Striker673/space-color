import pygame
from .game_state import GameState
from ..sprites.player import Player
from ..sprites.platform import Platform, MovingPlatform
from ..utils.constants import COLORS


class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = None
        self.init_level()

    def init_level(self) -> None:
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        ground = Platform(0, 700, 1280, 20, "blue")
        platform1 = Platform(300, 500, 200, 20, "red")
        platform2 = MovingPlatform(600, 400, 200, 20, "yellow", move_x=200)

        self.platforms.add(ground, platform1, platform2)
        self.all_sprites.add(ground, platform1, platform2)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            elif event.key == pygame.K_q:
                self.player.change_color("red")
            elif event.key == pygame.K_w:
                self.player.change_color("blue")
            elif event.key == pygame.K_e:
                self.player.change_color("yellow")
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state('menu')

    def update(self) -> None:
        self.all_sprites.update()
        self.handle_collisions()

    def handle_collisions(self) -> None:
        for platform in self.platforms:
            if pygame.sprite.collide_rect(self.player, platform):
                if self.player.color == platform.image.get_at((0, 0)):
                    if self.player.velocity_y > 0:
                        self.player.rect.bottom = platform.rect.top
                        self.player.velocity_y = 0
                else:
                    self.player.rect.x = 100
                    self.player.rect.y = 100
                    self.player.velocity_x = 0
                    self.player.velocity_y = 0

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(COLORS["black"])
        self.all_sprites.draw(screen)