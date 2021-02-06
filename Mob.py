from Constants import *
import pygame
import random


class Mob:
    def __init__(self, screen):
        self.screen = screen
        # self.image_pack = image_pack

        self.status = "friendly"

        self.health_point = MONSTER_HP

        self.moves = []
        self.active_move = {"Forward": False, "Back": False, "Right": False, "Left": False}
        self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])

        self.x = 500
        self.y = 200

        self.line_of_sight = MONSTER_LINE_OF_SIGHT

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

            print(self.status)

            if self.status == "friendly":
                self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])

        pygame.draw.rect(self.screen, pygame.Color('black'), (self.x, self.y, 30, 30))

        self.animation_counter += 1

    def get_mob_cords(self):
        return [self.x, self.y]

    def get_damage(self, damage):
        self.health_point -= damage

    def moving(self, player_cords=None):

        if self.status == "friendly":

            if self.move_choise == "Forward" and self.y + PLAYER_HITBOX_HEIGHT < SCREEN_HEIGHT - 5:
                self.y += MONSTER_SPEED

            elif self.move_choise == "Back" and self.y > 5:
                self.y -= MONSTER_SPEED

            elif self.move_choise == "Right" and self.x + PLAYER_HITBOX_WEIGHT < SCREEN_WEIGHT - 5:
                self.x += MONSTER_SPEED

            elif self.move_choise == "Left" and self.x > 5:
                self.x -= MONSTER_SPEED

        elif self.status == "aggressive":

            if self.y < player_cords[1] - MONSTER_SPEED + 20:
                self.y += MONSTER_SPEED
                self.move_choise = "Forward"

            elif self.y > player_cords[1] + 20:
                self.y -= MONSTER_SPEED
                self.move_choise = "Back"

            elif self.x < player_cords[0] - MONSTER_SPEED + 15:
                self.x += MONSTER_SPEED
                self.move_choise = "Right"

            elif self.x > player_cords[0] + 15:
                self.x -= MONSTER_SPEED
                self.move_choise = "Left"



