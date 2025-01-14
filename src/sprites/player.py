from utils.constants import COLORS
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.sprite_size = 64
        self.current_animation_time = 0

        self.is_jumping = False
        self.facing_right = True
        self.current_color = "red"

        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 7.5
        self.jump_power = -20.5
        self.gravity = 0.8
        self.can_jump = True

        self.run_tileset = None
        self.jump_tileset = None

        self.image = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.load_tileset()

    def load_tileset(self):
        self.run_tileset = pygame.Surface((self.sprite_size * 6, self.sprite_size), pygame.SRCALPHA)
        self.jump_tileset = pygame.Surface((self.sprite_size * 5, self.sprite_size), pygame.SRCALPHA)

        try:
            for i in range(6):
                try:
                    original_frame = pygame.image.load(
                        f"../assets/images/Astronaut_Run_{self.current_color.capitalize()}({i}).png").convert_alpha()

                    temp_surface = pygame.Surface(original_frame.get_size(), pygame.SRCALPHA)
                    temp_surface.blit(original_frame, (0, 0))

                    scaled_frame = pygame.transform.smoothscale(temp_surface, (self.sprite_size, self.sprite_size))
                    self.run_tileset.blit(scaled_frame, (i * self.sprite_size, 0))
                except Exception as e:
                    print(f"Error loading run frame {i}: {e}")
                    self.create_fallback_sprite()
                    return

            for i in range(5):
                try:
                    original_frame = pygame.image.load(
                        f"../assets/images/Astronaut_Jump_{self.current_color.capitalize()}({i}).png").convert_alpha()

                    temp_surface = pygame.Surface(original_frame.get_size(), pygame.SRCALPHA)
                    temp_surface.blit(original_frame, (0, 0))

                    scaled_frame = pygame.transform.smoothscale(temp_surface, (self.sprite_size, self.sprite_size))
                    self.jump_tileset.blit(scaled_frame, (i * self.sprite_size, 0))
                except Exception as e:
                    print(f"Error loading jump frame {i}: {e}")
                    self.create_fallback_sprite()
                    return

        except Exception as e:
            print(f"Error loading sprites: {e}")
            self.create_fallback_sprite()

    def create_fallback_sprite(self):
        self.run_tileset = pygame.Surface((self.sprite_size * 6, self.sprite_size), pygame.SRCALPHA)
        self.jump_tileset = pygame.Surface((self.sprite_size * 5, self.sprite_size), pygame.SRCALPHA)

        color = COLORS[self.current_color]
        rect_surface = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, color, rect_surface.get_rect())

        pygame.draw.rect(rect_surface, (255, 255, 255), rect_surface.get_rect(), 2)

        for tileset in [self.run_tileset, self.jump_tileset]:
            for i in range(tileset.get_width() // self.sprite_size):
                tileset.blit(rect_surface, (i * self.sprite_size, 0))

    def get_current_frame(self):
        frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        current_frame_x = 0

        if self.is_jumping:
            if self.velocity_y < 0:
                current_frame_x = self.sprite_size
            else:
                current_frame_x = self.sprite_size * 3
            frame.blit(self.jump_tileset, (0, 0), (current_frame_x, 0, self.sprite_size, self.sprite_size))
        else:
            if abs(self.velocity_x) > 0:
                self.current_animation_time = pygame.time.get_ticks()
                current_frame_x = ((self.current_animation_time // 100) % 6) * self.sprite_size
            frame.blit(self.run_tileset, (0, 0), (current_frame_x, 0, self.sprite_size, self.sprite_size))

        # Apply direction
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def update(self) :
        self.apply_gravity()
        self.handle_movement()
        self.image = self.get_current_frame()
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def handle_movement(self) :
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True

    def change_color(self, color_name: str) :
        if color_name in COLORS and color_name != self.current_color:
            old_facing = self.facing_right
            old_jumping = self.is_jumping
            self.current_color = color_name
            self.load_tileset()
            self.facing_right = old_facing
            self.is_jumping = old_jumping
            self.image = self.get_current_frame()

    def apply_gravity(self) :
        self.velocity_y += self.gravity

    def jump(self) :
        if self.can_jump:
            self.velocity_y = self.jump_power
            self.can_jump = False
            self.is_jumping = True
