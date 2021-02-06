import pygame
from Constants import *
from Player import Hero
from Mob import *


class Menu:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.window_surface = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))

        self.background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.background.fill(pygame.Color((40, 40, 40)))

        self.newgame_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/New Game Button.png"), (150, 70))
        self.levels_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Levels Button.png"), (150, 70))
        self.options_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Options Button.png"), (150, 70))
        self.exit_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Exit Button.png"), (150, 70))

        self.background.blit(self.newgame_btn, (430, 300))
        self.background.blit(self.levels_btn, (430, 400))
        self.background.blit(self.options_btn, (430, 500))
        self.background.blit(self.exit_btn, (430, 600))

        self.running = True

    def main(self):
        all_sprites = pygame.sprite.Group()
        cursor = Cursor(all_sprites)

        while self.running:
            pygame.time.Clock().tick(FPS)
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION:
                    cursor.update(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 430 <= event.pos[0] <= 450 + 150 and 300 <= event.pos[1] <= 300 + 70:
                        self.running = False
                        World(screen).main_loop()
                    if 430 <= event.pos[0] <= 450 + 150 and 400 <= event.pos[1] <= 400 + 70:
                        print('levels')
                    if 430 <= event.pos[0] <= 450 + 150 and 500 <= event.pos[1] <= 500 + 70:
                        print('options')
                    if 430 <= event.pos[0] <= 450 + 150 and 600 <= event.pos[1] <= 600 + 70:
                        self.running = False
                if key[pygame.K_ESCAPE]:
                    self.running = False

                self.window_surface.blit(self.background, (0, 0))

            if pygame.mouse.get_focused():
                all_sprites.draw(screen)

            pygame.display.update()
        pygame.quit()


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super(Cursor, self).__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("Resources/Main menu/cursor.png").convert_alpha(), (35, 40))
        self.rect = self.image.get_rect()

    def update(self, coord_):
        self.rect.topleft = coord_


class World:
    def __init__(self, screen):
        pygame.mouse.set_visible(True)

        self.screen = screen
        self.background = pygame.image.load(BACK_GROUND[0])
        self.running = True
        self.player = Hero(self.screen)
        self.mob = Crocodile(self.screen)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render()
        self.mob.render()
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
    Menu().main()
    # World(screen).main_loop()
