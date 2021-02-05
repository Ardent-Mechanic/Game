from Constants import *
import pygame
import random


class Mob:
    def __init__(self, screen):
        self.screen = screen
        # self.image_pack = image_pack

        self.health_point = MONSTER_HP

        self.moves = []
        self.active_move = {"Forward": False, "Back": False, "Right": False, "Left": False}
        self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])

        self.x = 500
        self.y = 200

        self.line_of_sight = 250

        self.animation_counter = MAX_FRAMES_FOR_IMAGE

        # image = pygame.image.load(self.image_pack[0]).convert_alpha()
        #
        # pose = pygame.transform.scale(image.subsurface(43, 0, 49, 69), (50, 70))
        #
        # self.moves.append(pose)
        #
        # self.screen.blit(self.moves[0], (self.x, self.y))

    def render(self):

        if self.animation_counter + 1 >= 3 * MAX_FRAMES_FOR_IMAGE:
            self.animation_counter = 0
            self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])

        pygame.draw.rect(self.screen, pygame.Color('black'), (self.x, self.y, 30, 30))

        self.animation_counter += 1

    # def chek_active_move(self, skip_key):
    #     for key in self.active_move.keys():
    #         if key != skip_key:
    #             self.active_move[key] = False

    def get_mob_cords(self):
        return [self.x, self.y]

    def get_damage(self, damage):
        self.health_point -= damage

    def moving(self):
        if self.move_choise == "Forward" and self.y + PLAYER_HITBOX_HEIGHT < SCREEN_HEIGHT - 5:
            self.y += MONSTER_SPEED

        elif self.move_choise == "Back" and self.y > 5:
            self.y -= MONSTER_SPEED

        elif self.move_choise == "Right" and self.x + PLAYER_HITBOX_WEIGHT < SCREEN_WEIGHT - 5:
            self.x += MONSTER_SPEED

        elif self.move_choise == "Left" and self.x > 5:
            self.x -= MONSTER_SPEED
