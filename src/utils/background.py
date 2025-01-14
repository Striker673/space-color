import pygame
import random
import math


class Star:
    def __init__(self, x: float, y: float, speed: float, direction: int):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.trail = [(x, y)]
        self.trail_length = 20
        self.alive = True
        self.radius = 1
        self.exploding = False
        self.explosion_radius = 0
        self.max_explosion_radius = 30
        self.explosion_speed = 2

    def update(self) -> None:
        if self.exploding:
            self.update_explosion()
        else:
            self.update_movement()

    def update_movement(self) -> None:
        self.x += self.speed * self.direction

        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def update_explosion(self) -> None:
        self.explosion_radius += self.explosion_speed
        if self.explosion_radius >= self.max_explosion_radius:
            self.alive = False

    def check_collision(self, stars: list['Star']) -> None:
        if self.exploding:
            return

        for star in stars:
            if star != self and not star.exploding:
                distance = math.hypot(self.x - star.x, self.y - star.y)
                if distance < self.radius * 2:
                    self.exploding = True
                    star.exploding = True

    def draw(self, screen: pygame.Surface) -> None:
        if self.exploding:
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), int(self.explosion_radius))
        else:
            if len(self.trail) > 1:
                pygame.draw.lines(screen, (150, 150, 150), False, self.trail, 1)

            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)


class BackgroundManager:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.stars = []
        self.star_spawn_rate = 0.02
        self.max_stars = 50
        self.bg_image = None
        self.parallax_factor = 0.5
        self.current_bg_number = -1
        self.load_random_background(force_new=True)

    def load_random_background(self, force_new=False):
        try:
            if force_new:
                new_bg_number = self.current_bg_number
                while new_bg_number == self.current_bg_number:
                    new_bg_number = random.randint(0, 16)
                self.current_bg_number = new_bg_number

            original_image = pygame.image.load(f"../assets/images/Space Background({self.current_bg_number}).png")
            height = self.height
            width = int(original_image.get_width() * (height / original_image.get_height()))
            self.bg_image = pygame.transform.scale(original_image, (width, height))

        except Exception as e:
            print(f"Error loading background: {e}")
            self.bg_image = pygame.Surface((self.width, self.height))
            self.bg_image.fill((0, 0, 30))

    def change_background(self):
        self.load_random_background(force_new=True)

    def update(self) -> None:
        if len(self.stars) < self.max_stars and random.random() < self.star_spawn_rate:
            y = random.randint(0, self.height)
            speed = random.uniform(3, 7)

            if random.random() < 0.5:
                self.stars.append(Star(0, y, speed, 1))
            else:
                self.stars.append(Star(self.width, y, speed, -1))

        for star in self.stars:
            star.update()
            star.check_collision(self.stars)

        self.stars = [star for star in self.stars if (0 < star.x < self.width) and star.alive]

    def draw(self, screen: pygame.Surface, camera_x: float = 0):
        bg_x = -camera_x * self.parallax_factor
        bg_x = max(-(self.bg_image.get_width() - self.width), min(0, bg_x))
        screen.blit(self.bg_image, (bg_x, 0))

        for star in self.stars:
            star.draw(screen)
