import pygame
from Constants import *


class World:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(BACK_GROUND[0])
        self.running = True

    def render(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            com = pygame.key.get_pressed()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    wordl_start = World(screen).main_loop()
