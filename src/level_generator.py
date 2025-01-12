import random
from sprites.platform import Platform, MovingPlatform
from sprites.collectible import Collectible, LevelEndOrb

class LevelGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.platform_colors = ["red", "yellow", "blue"]
        self.min_platform_width = 100
        self.max_platform_width = 300
        self.min_gap = 100
        self.max_gap = 200
        self.platform_height = 20

    def generate_platforms(self, num_platforms: int):
        platforms = []
        collectibles = []
        last_x = 0
        last_y = self.height - 100
        max_x_position = self.width - 500

        platforms.append(Platform(0, self.height - 50, 300, 20, "red"))

        for i in range(num_platforms):
            width = random.randint(self.min_platform_width, self.max_platform_width)
            gap = random.randint(self.min_gap, self.max_gap)
            x = min(last_x + gap + width, max_x_position)

            if x >= max_x_position:
                platform = Platform(x - width, last_y, width, self.platform_height,random.choice(self.platform_colors))
                platforms.append(platform)
                end_orb = LevelEndOrb(x - width//2, last_y - 50)
                collectibles.append(end_orb)
                break

            max_height_change = 150
            y = max(100, min(self.height - 100,
                           last_y + random.randint(-max_height_change, max_height_change)))

            color = random.choice(self.platform_colors)

            if random.random() < 0.3:
                platform = MovingPlatform(x, y, width, self.platform_height, color,move_x=random.randint(100, 200))
            else:
                platform = Platform(x, y, width, self.platform_height, color)

            platforms.append(platform)

            if random.random() < 0.5 and i < num_platforms - 1:
                collectible = Collectible(x + width // 2, y - 50, color)
                collectibles.append(collectible)

            last_x = x
            last_y = y

        if last_x < max_x_position and not any(isinstance(c, LevelEndOrb) for c in collectibles):
            final_x = min(last_x + gap + width, max_x_position)
            final_platform = Platform(final_x - width, last_y, width, self.platform_height,
                                  random.choice(self.platform_colors))
            platforms.append(final_platform)
            end_orb = LevelEndOrb(final_x - width//2, last_y - 50)
            collectibles.append(end_orb)

        return platforms, collectibles
