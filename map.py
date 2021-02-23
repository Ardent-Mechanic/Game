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
    def __init__(self, number, screen):

        self.screen = screen

        self.level_number = number

        self.tile_size = 32

        """Test size"""
        self.height = SCREEN_HEIGHT // self.tile_size
        self.width = SCREEN_WEIGHT // self.tile_size
        """Test size"""

        self.background_cords = []
        self.walls_cords = []

        self.background_pic = Image.new('RGB', (SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.walls_pic = Image.new('RGB', (SCREEN_WEIGHT, SCREEN_HEIGHT))

    def render_world(self):
        self.screen.blit(self.background_pic, (0, 0))
        self.screen.blit(self.walls_pic, (0, 0))

    def csv_reader(self):

        with open(f"Resources/maps/{self.level_number}/background.csv") as bg:
            data = csv.reader(bg, delimiter=",")
            for row in data:
                self.background_cords.append(list(map(int, row)))

        with open(f"Resources/maps/{self.level_number}/walls.csv") as walls:
            data = csv.reader(walls, delimiter=",")
            for row in data:
                self.walls_cords.append(list(map(int, row)))

    def pilImageToSurface(self, pill_image):
        return pygame.image.fromstring(
            pill_image.tobytes(), pill_image.size, pill_image.mode).convert()

    def give_level_element(self):
        return self.pilImageToSurface(self.background_pic), self.pilImageToSurface(self.walls_pic)

    def load_tiles(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.walls_cords[row][col] != -1:
                    img_num = self.walls_cords[row][col]
                    self.walls_pic.paste(
                        Image.open(f"Resources/tileset/{img_num}.png").resize((32, 32), Image.ANTIALIAS),
                        (col * 32, row * 32))

        for row in range(self.height):
            for col in range(self.width):
                if self.background_cords[row][col] != -1:
                    img_num = self.background_cords[row][col]
                    self.background_pic.paste(
                        Image.open(f"Resources/tileset/{img_num}.png").resize((32, 32), Image.ANTIALIAS),
                        (col * 32, row * 32))
        self.walls_pic.save("123.png")

    def create_map(self):
        self.csv_reader()
        self.load_tiles()
        self.background_pic, self.walls_pic = self.give_level_element()


if __name__ == '__main__':
    # boom.render_world()
    pygame.init()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)

    boom = Map(1, screen)
    boom.create_map()
    boom.render_world()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        boom.render_world()
        pygame.display.flip()
    pygame.quit()
