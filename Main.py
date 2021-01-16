import pygame
from Constants import *
from Player import Hero


class World:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.background = pygame.image.load(BACK_GROUND[0])
        self.running = True
        self.player = Hero(self.screen)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render()
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            com = pygame.key.get_pressed()
            self.player.moving(com)
            self.render()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    # screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    # player = Hero(screen).filling_moves()
    # wordl_start = World(screen).main_loop()
