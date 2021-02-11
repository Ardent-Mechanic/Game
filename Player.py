from Constants import *
import pygame


class Hero:
    def __init__(self, screen):

        self.screen = screen

        self.health_bar = None
        self.health_point = HP

        self.mana_bar = None
        self.mana_point = MANA

        self.moves = []
        self.attack_moves = []
        self.death_animation = None
        self.active_move = {"Forward": False, "Back": False, "Right": False, "Left": False, "Attack": False}
        self.previous_active_move = "Forward"
        self.animation_counter = 0

        self.x = 50
        self.y = 50

    def filling_moves(self):
        images = ["Resources/test_forward.png", "Resources/test_back.png",
                  "Resources/test_right.png", "Resources/test_left.png"]

        for link in images:
            image = pygame.image.load(link).convert_alpha()
            pose1 = pygame.transform.scale(image.subsurface(0, 0, 28, 34), PLAYER_SIZE)
            pose2 = pygame.transform.scale(image.subsurface(28, 0, 28, 34), PLAYER_SIZE)
            pose3 = pygame.transform.scale(image.subsurface(56, 0, 28, 34), PLAYER_SIZE)

            self.moves.append([pose1, pose2, pose3, pose2])

        images = ["Resources/forward_attak.png", "Resources/back_attak.png",
                  "Resources/right_attak.png", "Resources/left_attak.png"]

        for link in images:
            image = pygame.image.load(link).convert_alpha()
            pose1 = pygame.transform.scale(image.subsurface(28, 0, 28, 34), PLAYER_SIZE)
            pose2 = pygame.transform.scale(image.subsurface(56, 0, 28, 34), PLAYER_SIZE)
            pose3 = pygame.transform.scale(image.subsurface(84, 0, 28, 34), PLAYER_SIZE)

            self.attack_moves.append([pose1, pose2, pose3])

        imgs = pygame.image.load("Resources/health_and_mana_bar.png").convert_alpha()
        self.health_bar, self.mana_bar = imgs.subsurface(0, 0, 249, 29), imgs.subsurface(0, 25, 249, 28)

        self.death_animation = pygame.transform.scale(pygame.image.load("Resources/PLITA.png"), (28 * 2, 34 * 2))

    def render(self):

        if self.active_move["Attack"]:

            if self.animation_counter + 1 >= len(self.attack_moves[0]) * MAX_FRAMES_FOR_IMAGE:

                if self.active_move["Attack"]:
                    self.active_move["Attack"] = False

                    # self.give_damage("z", self.previous_active_move)

                    self.change_mana("Attack")
                    self.active_move[self.previous_active_move] = True

                self.animation_counter = 0

            self.screen.blit(self.attack_moves[list(self.active_move.keys()).index(self.previous_active_move)][
                                 self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))

        else:
            if self.animation_counter + 1 >= len(self.moves[0]) * MAX_FRAMES_FOR_IMAGE:
                self.animation_counter = 0

            if self.active_move["Forward"]:
                self.screen.blit(self.moves[0][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))
                self.previous_active_move = "Forward"

            elif self.active_move["Back"]:
                self.screen.blit(self.moves[1][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))
                self.previous_active_move = "Back"

            elif self.active_move["Right"]:
                self.screen.blit(self.moves[2][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))
                self.previous_active_move = "Right"

            elif self.active_move["Left"]:
                self.screen.blit(self.moves[3][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))
                self.previous_active_move = "Left"

            else:
                self.screen.blit(self.moves[list(self.active_move.keys()).index(self.previous_active_move)][1],
                                 (self.x, self.y))
                self.animation_counter = 0

        self.animation_counter += 1

    def chek_active_move(self, skip_key):
        for key in self.active_move.keys():
            if key != skip_key:
                self.active_move[key] = False

    def get_player_cords(self):
        return [self.x, self.y]

    def get_damage(self, damage):
        self.health_point -= damage

    def give_damage(self, button_name, side):
        cords = []

        if side == "Forward":
            cords = [self.x, self.y + 60, 50, 20]
        elif side == "Back":
            cords = [self.x, self.y - 5, 50, 20]
        elif side == "Left":
            cords = [self.x - 10, self.y - 5, 20, 70]
        elif side == "Right":
            cords = [self.x + 43, self.y - 5, 20, 70]

        """Проверка длинны радиуса атаки"""
        pygame.draw.rect(self.screen, pygame.Color("Yellow"), cords, 2)

        if button_name == "z":
            return [5, cords]

    def change_mana(self, pressed_button):
        if pressed_button == "Attack":
            self.mana_point -= 22

    def hp_regen(self):
        self.health_point += HP_REGEN

    def mn_regen(self):
        self.mana_point += MN_REGEN

    def moving(self, pressed_button):
        skip_key = "None"

        if pressed_button[pygame.K_LEFT] and self.x > 5:
            self.x -= SPEED
            self.active_move["Left"] = True
            skip_key = "Left"

        elif pressed_button[pygame.K_RIGHT] and self.x + PLAYER_HITBOX_WEIGHT < SCREEN_WEIGHT - 5:
            self.x += SPEED
            self.active_move["Right"] = True
            skip_key = "Right"

        elif pressed_button[pygame.K_UP] and self.y > 5:
            self.y -= SPEED
            self.active_move["Back"] = True
            skip_key = "Back"

        elif pressed_button[pygame.K_DOWN] and self.y + PLAYER_HITBOX_HEIGHT < SCREEN_HEIGHT - 5:
            self.y += SPEED
            self.active_move["Forward"] = True
            skip_key = "Forward"

        elif pressed_button[pygame.K_z]:
            if self.mana_point > 0:
                self.active_move["Attack"] = True
                skip_key = "Attack"

        elif pressed_button[pygame.K_SPACE]:
            self.get_damage(5)

        self.chek_active_move(skip_key)
