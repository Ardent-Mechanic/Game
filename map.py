import pygame
import csv
from Constants import *
from PIL import Image


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

        self.background_pic = Image.new('RGBA', (SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.walls_pic = Image.new('RGBA', (SCREEN_WEIGHT, SCREEN_HEIGHT))

    def csv_reader(self):

        with open(f"Resources/maps/{self.level_number}/background.csv") as bg:
            data = csv.reader(bg, delimiter=",")
            for row in data:
                self.background_cords.append(list(map(int, row)))

        with open(f"Resources/maps/{self.level_number}/walls.csv") as walls:
            data = csv.reader(walls, delimiter=",")
            for row in data:
                self.walls_cords.append(list(map(int, row)))

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

        self.background_pic.paste(self.walls_pic, (0, 0), self.walls_pic)
        self.background_pic.save(f"Resources/maps/{self.level_number}/background.png")

    def create_map(self):
        self.csv_reader()
        self.load_tiles()
        self.background_pic = pygame.image.load(f"Resources/maps/{self.level_number}/background.png")

    def chek_postion(self, cords):
        col1, col2 = (cords[0] - 3) // self.tile_size, (cords[2] - 3) // self.tile_size
        row1, row2 = (cords[1] - 6) // self.tile_size, (cords[3] + 6) // self.tile_size
        return (self.walls_cords[row1][col1] == -1 and self.walls_cords[row2][col2] == -1) \
               or (self.walls_cords[row1][col2] == -1 and self.walls_cords[row2][col1] == -1)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)

    boom = Map(1, screen)
    boom.create_map()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(boom.background_pic, (0, 0))
        pygame.display.flip()
    pygame.quit()
