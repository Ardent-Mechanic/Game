import pygame
# import pytmx
import csv
from Constants import *
from PIL import Image


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 32

        """Test size"""
        self.height = SCREEN_HEIGHT // self.tile_size
        self.width = SCREEN_WEIGHT // self.tile_size
        """Test size"""

        self.background = []
        self.walls_tiles = []

    def render_world(self):
        for y in range(self.height):
            for x in range(self.width):
                pass
            # gg =pygame.transform.scale(img, (32, 32))
            # self.screen.blit(img, (x * self.tile_size, y * self.tile_size))

    def csv_reader(self, num):
        background, walls_box = [], []

        with open(f"Resources/maps/{num}/new_background.csv") as bg:
            data = csv.reader(bg, delimiter=",")
            for row in data:
                self.background.append(list(row))

        with open(f"Resources/maps/{num}/new_walls.csv") as walls:
            data = csv.reader(walls, delimiter=",")
            for row in data:
                self.walls_tiles.append(list(row))

    def load_tiles(self, num):
        pass


boom = Map(pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT)))
boom.render_world()
