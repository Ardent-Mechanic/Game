import pygame
from Constants import *
from Player import Hero


class World:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(BACK_GROUND[0])
        self.running = True
        self.player = Hero(self.screen)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render()
        pygame.display.flip()

    def main_loop(self):
        self.player.filling_moves()

        while self.running:
            pygame.time.Clock().tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            com = pygame.key.get_pressed()
            self.player.moving(com)
            self.render()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    # player = Hero(screen).filling_moves()
    World(screen).main_loop()
