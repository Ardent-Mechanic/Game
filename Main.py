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
        self.options_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Options Button.png"), (150, 70))
        self.exit_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Exit Button.png"), (150, 70))

        self.background.blit(self.newgame_btn, (430, 300))
        self.background.blit(self.options_btn, (430, 400))
        self.background.blit(self.exit_btn, (430, 500))

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
                        print('2')
                    if 430 <= event.pos[0] <= 450 + 150 and 500 <= event.pos[1] <= 500 + 70:
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

        self.mob = Mob(self.screen)

    def render(self, com):
        self.screen.blit(self.background, (0, 0))

        if self.player.health_point <= 0:
            self.screen.blit(self.player.death_animation, (self.player.x, self.player.y))
        else:
            self.player.moving(com)
            self.player.render()

        self.screen.blit(self.player.health_bar, HEALTH_BAR_CORDS)

        """Дамаг и трата стамины немного неправильно рисуются. Переписать."""

        if self.player.health_point > 0:
            pygame.draw.rect(self.screen, pygame.Color(160, 55, 53),
                             (775 + 3 + self.player.health_point,
                              HEALTH_BAR_CORDS[1] + 3, HP - self.player.health_point, 22))

        self.screen.blit(self.player.mana_bar, MANA_BAR_CORDS)

        if self.player.mana_point > 0:
            pygame.draw.rect(self.screen, pygame.Color(45, 123, 163),
                             (775 + 3 + self.player.mana_point,
                              MANA_BAR_CORDS[1] + 3, MANA - self.player.mana_point, 22))

        if self.mob.health_point <= 0:
            pygame.draw.rect(self.screen, pygame.Color("white"), (self.mob.x, self.mob.y, 30, 30))
        else:
            self.mob.moving()

            pygame.draw.rect(self.screen, pygame.Color("Red"), (self.mob.x - 10, self.mob.y - 10, 50, 3))

            self.mob.render()

    def main_loop(self):
        self.player.filling_moves()

        while self.running:
            pygame.time.Clock().tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            com = pygame.key.get_pressed()

            if com[pygame.K_r]:
                self.player.x = self.player.y = 50
                self.player.health_point = HP
                self.player.mana_point = MANA

            self.render(com)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    # player = Hero(screen).filling_moves()
    Menu().main()
    # World(screen).main_loop()
