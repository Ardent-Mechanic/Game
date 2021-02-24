import pygame
from Constants import *
from Player import Hero
from Mob import *
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


class WindowAfterDeath:
    def __init__(self):
        pygame.mouse.set_visible(True)
        self.window_surface = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))

        self.background = pygame.Surface((SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.background.fill(pygame.Color(40, 40, 40))
        img = pygame.transform.scale(pygame.image.load("Resources/Main menu/game_over.png"), (250, 250))

        self.background.blit(img, (SCREEN_WEIGHT // 2 - 140, SCREEN_HEIGHT // 2 - 250))
        self.background.blit(pygame.image.load("Resources/Main menu/restart.png"), (180, SCREEN_HEIGHT // 2))

        self.running = True

    def main(self):

        while self.running:
            pygame.time.Clock().tick(FPS)
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if key[pygame.K_r]:
                    World(screen).main_loop()

                if key[pygame.K_ESCAPE]:
                    self.running = False

            self.window_surface.blit(self.background, (0, 0))

            pygame.display.update()
        pygame.quit()


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super(Cursor, self).__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("Resources/Main menu/cursor1.png").convert_alpha(),
                                            (35, 40))
        self.rect = self.image.get_rect()

    def update(self, coord_):
        self.rect.topleft = coord_


class World:
    def __init__(self, screen):
        # pygame.mouse.set_visible(True)

        self.screen = screen

        self.running = True

        self.weight = SCREEN_WEIGHT // 16

        self.height = SCREEN_HEIGHT // 16

        with open("level_number.txt", mode="r", encoding="utf8") as lvl:
            self.level = int(lvl.read().strip())

        self.lvl_info = LVL[self.level - 1]

        self.player = Hero(self.screen, self.lvl_info["PLAYER_CORD"])

        self.mob_box = [Mob(self.screen, mob_type, cords) for mob_type, cords in self.lvl_info["MONSTERS"]]

        self.map = Map(self.level, screen)

        self.window = WindowAfterDeath()

        self.damage_sound = pygame.mixer.Sound('Resources/sound/damage.mp3')
        self.damage_sound.set_volume(10.0)

    def render_models(self, com):

        self.screen.blit(self.map.background_pic, (0, 0))

        if self.player.health_point <= 0:
            self.screen.blit(self.player.death_animation, (self.player.x, self.player.y))
            self.window.main()

        else:
            x, y = self.player.get_player_cords()

            self.player.moving(com)

            self.player.render()

        if self.player.health_point != HP:
            self.player.hp_regen()

        if self.player.mana_point != MANA:
            self.player.mn_regen()

        self.screen.blit(self.player.health_bar, HEALTH_BAR_CORDS)

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

                # self.damage_sound.play()

                for mob in self.mob_box:
                    if (mob.x <= attack_cords[0] <= mob.x + MONSTER_HITBOX_WEIGHT or attack_cords[0] <= mob.x <=
                        attack_cords[0] + attack_cords[2]) and (
                            mob.y <= attack_cords[1] <= mob.y + MONSTER_HITBOX_HEIGHT or attack_cords[1] <= mob.y <=
                            attack_cords[1] + attack_cords[3]):
                        self.damage_sound.play()
                        mob.get_damage(damage)

                self.player.damage_counter = 10

            self.player.damage_counter -= 1

        for index, mob in enumerate(self.mob_box[::]):

            pygame.draw.rect(self.screen, pygame.Color("black"), (mob.x - 10, mob.y - 10, 50, 3))

            if mob.health_point <= 0:
                pygame.draw.rect(self.screen, pygame.Color("white"), (mob.x, mob.y, 30, 30))
                del self.mob_box[index]

            else:

                pygame.draw.rect(self.screen, pygame.Color("red"), (mob.x - 10, mob.y - 10, mob.health_point, 3))

                if mob.status == "friendly":
                    mob.moving()

                elif mob.status == "aggressive":
                    mob.moving(self.player.get_player_cords())

                elif mob.status == "attack":

                    if mob.damage_counter == 0:
                        self.player.get_damage(mob.damage)
                        mob.damage_counter = 20

                    mob.damage_counter -= 1

                mob.render()

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('Resources/sound/bg_music.mp3')
        pygame.mixer.music.play(10)

    def main_loop(self):

        self.player.filling_moves()

        [mob.filling_moves() for mob in self.mob_box]

        self.map.create_map()

        self.player.wall_box = self.map.walls_cords

        self.play_music()

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

            self.render_models(com)

            if len(self.mob_box) == 0:
                with open("level_number.txt", mode="w", encoding="utf8") as lvl:
                    lvl.write(str(self.level + 1))
                World(screen).main_loop()

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    Menu().main()
