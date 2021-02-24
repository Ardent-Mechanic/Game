import pygame
from Constants import *
from Player import Hero
from Mob import *
import pytmx
from map import Map


class Menu:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.window_surface = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))

        self.background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.background.fill(pygame.Color((40, 40, 40)))

        self.newgame_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/New Game Button.png"),
                                                  (150, 70))
        self.options_btn = pygame.transform.scale(pygame.image.load("Resources/Main menu/Options Button.png"),
                                                  (150, 70))
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
        self.image = pygame.transform.scale(pygame.image.load("Resources/Main menu/cursor.png").convert_alpha(),
                                            (35, 40))
        self.rect = self.image.get_rect()

    def update(self, coord_):
        self.rect.topleft = coord_


class World:
    def __init__(self, screen):
        pygame.mouse.set_visible(True)

        self.screen = screen

        self.running = True

        self.weight = SCREEN_WEIGHT // 16

        self.height = SCREEN_HEIGHT // 16

        self.player = Hero(self.screen)

        self.mob = Mob(self.screen, "snake")

        self.mob_box = [Mob(self.screen, "fire")]

        self.map = Map(1, screen)

    def render_models(self, com):

        self.screen.blit(self.map.background_pic, (0, 0))

        if self.player.health_point != HP:
            self.player.hp_regen()

        if self.player.mana_point != MANA:
            self.player.mn_regen()

        if self.player.health_point <= 0:
            self.screen.blit(self.player.death_animation, (self.player.x, self.player.y))
        else:
            x, y = self.player.get_player_cords()
            # cords = self.player.chek_moving(com)
            # print(cords)

            # if cords:
            #     if self.map.chek_postion(cords):
            #         self.player.moving(com)
            # else:
            self.player.moving(com)
            # else:
            #     pass

            # self.player.moving(com)

            if com[pygame.K_LEFT]:
                # pygame.draw.rect(self.screen, pygame.Color("yellow"), (x + 4, y + 48, 26, 12), 1)
                pygame.draw.rect(self.screen, pygame.Color("yellow"), (x + 4, y + 48, 26, 12), 1)
                # pygame.draw.rect(self.screen, pygame.Color("red"), (x + 12, y - 2, 26, 62), 1)
            elif com[pygame.K_RIGHT]:
                pygame.draw.rect(self.screen, pygame.Color("yellow"), (x + 26, y + 48, 26, 12), 1)
                # pygame.draw.rect(self.screen, pygame.Color("red"), (x + 22, y - 2, 26, 62), 1)
            elif com[pygame.K_UP]:
                pygame.draw.rect(self.screen, pygame.Color("yellow"), (x + 16, y + 42, 20, 10), 1)
                # pygame.draw.rect(self.screen, pygame.Color("red"), (x + 12, y - 2, 26, 62), 1)
            else:
                pygame.draw.rect(self.screen, pygame.Color("yellow"), (x + 16, y + 52, 20, 10), 1)
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

        if self.player.active_move["Attack"]:

            if self.player.damage_counter == 0:
                damage, attack_cords = self.player.give_damage("z", self.player.previous_active_move)

                [
                    mob.get_damage(damage) for mob in self.mob_box if
                    (mob.x <= attack_cords[0] <= mob.x + MONSTER_HITBOX_WEIGHT
                     or attack_cords[0] <= mob.x <= attack_cords[0] + attack_cords[2]) and
                    (mob.y <= attack_cords[1] <= mob.y + MONSTER_HITBOX_HEIGHT
                     or attack_cords[1] <= mob.y <= attack_cords[1] + attack_cords[3])
                ]

                self.player.damage_counter = 10

            self.player.damage_counter -= 1

        for mob in self.mob_box:
            x_mob, y_mob = mob.get_mob_cords()

            pygame.draw.rect(self.screen, pygame.Color("black"), (mob.x - 10, mob.y - 10, 50, 3))

            if mob.health_point <= 0:
                pygame.draw.rect(self.screen, pygame.Color("white"), (mob.x, mob.y, 30, 30))

            else:

                pygame.draw.rect(self.screen, pygame.Color("red"), (mob.x - 10, mob.y - 10, mob.health_point, 3))

                if mob.status == "friendly":
                    mob.moving()

                elif mob.status == "aggressive":
                    # x_mob, y_mob = mob.get_mob_cords()
                    # x_player, y_player = self.player.get_player_cords()
                    mob.moving(self.player.get_player_cords())

                elif mob.status == "attack":

                    if mob.damage_counter == 0:
                        self.player.get_damage(mob.damage)
                        mob.damage_counter = 20

                    mob.damage_counter -= 1

                mob.render()

    def main_loop(self):

        self.player.filling_moves()

        [mob.filling_moves() for mob in self.mob_box]

        self.map.create_map()

        self.player.wall_box = self.map.walls_cords

        for mob in self.mob_box:
            mob.wall_box = self.map.walls_cords

        while self.running:
            pygame.time.Clock().tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            x_player, y_player = player_cords = self.player.get_player_cords()

            for mob in self.mob_box:
                n = mob.line_of_sight
                x_mob, y_mob = mob.get_mob_cords()

                if x_player + 50 >= x_mob >= x_player - 30 \
                        and y_player + 20 >= y_mob >= y_player - 30:
                    mob.status = "attack"

                elif x_mob + n >= player_cords[0] >= x_mob - n and y_mob + n >= player_cords[1] >= y_mob - n:
                    mob.status = "aggressive"

                else:

                    if mob.status != "friendly":
                        mob.status = "friendly"

            com = pygame.key.get_pressed()

            if com[pygame.K_r]:
                self.player.x = self.player.y = 100
                self.player.health_point = HP
                self.player.mana_point = MANA
                for mob in self.mob_box:
                    mob.health_point = MONSTER_HP

            self.render_models(com)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    Menu().main()
