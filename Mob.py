from Constants import *
import pygame
import random


class Mob:
    def __init__(self, screen, type):
        self.screen = screen
        # self.image_pack = image_pack

        self.type = type

        self.status = "friendly"

        self.health_point = MONSTER_HP

        self.moves = []
        self.active_move = {"Forward": False, "Back": False, "Right": False, "Left": False}
        self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])
        # self.previous_active_move = "Forward"

        self.damage = 50

        self.x = 500
        self.y = 200

        self.line_of_sight = MONSTER_LINE_OF_SIGHT

        self.animation_counter = MAX_FRAMES_FOR_IMAGE

        self.damage_counter = 10

        self.wall_box = []
        # image = pygame.image.load(self.image_pack[0]).convert_alpha()
        #
        # pose = pygame.transform.scale(image.subsurface(43, 0, 49, 69), (50, 70))
        #
        # self.moves.append(pose)
        #
        # self.screen.blit(self.moves[0], (self.x, self.y))

    def filling_moves(self):
        print(f"Resources/monsters_sprites/{self.type}/{self.type}_forward.png")
        images = [f"Resources/monsters_sprites/{self.type}/{self.type}_forward.png",
                  f"Resources/monsters_sprites/{self.type}/{self.type}_back.png",
                  f"Resources/monsters_sprites/{self.type}/{self.type}_right.png",
                  f"Resources/monsters_sprites/{self.type}/{self.type}_left.png"]

        for link in images:
            image = pygame.image.load(link).convert_alpha()
            pose1 = pygame.transform.scale(image.subsurface(0, 0, 26, 26), MONSTER_SIZE)
            pose2 = pygame.transform.scale(image.subsurface(26, 0, 26, 26), MONSTER_SIZE)
            pose3 = pygame.transform.scale(image.subsurface(52, 0, 26, 26), MONSTER_SIZE)

            self.moves.append([pose1, pose2, pose3, pose2])

    def render(self):
        if self.animation_counter + 1 >= len(self.moves[0]) * MAX_FRAMES_FOR_IMAGE:
            self.animation_counter = 0

            if self.status == "friendly":
                self.move_choise = random.choice(["Forward", "Back", "Right", "Left"])
                self.active_move[self.move_choise] = True
                self.chek_active_move(self.move_choise)

            elif self.status == "aggressive":
                self.active_move[self.move_choise] = True
                self.chek_active_move(self.move_choise)

        if self.active_move["Forward"]:
            self.screen.blit(self.moves[0][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))

        elif self.active_move["Back"]:
            self.screen.blit(self.moves[1][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))

        elif self.active_move["Right"]:
            self.screen.blit(self.moves[2][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))

        elif self.active_move["Left"]:
            self.screen.blit(self.moves[3][self.animation_counter // MAX_FRAMES_FOR_IMAGE], (self.x, self.y))

        self.animation_counter += 1

    def get_mob_cords(self):
        return [self.x, self.y]

    def get_damage(self, damage):
        self.health_point -= damage

    def give_damage(self, player):
        player.health_point -= self.damage

    def chek_active_move(self, skip_key):
        for key in self.active_move.keys():
            if key != skip_key:
                self.active_move[key] = False

    def chek_collisions(self, c1, r1, c2, r2):
        return self.wall_box[r1][c1] == -1 and self.wall_box[r1][c2] == -1 \
               and self.wall_box[r2][c1] == -1 and self.wall_box[r2][c2]

    def get_collision_box(self):
        if self.active_move["Left"]:
            cords = [self.x + 12, self.y + 48, self.x + 12 + 26, self.y + 48 + 12]
            # cords = [self.x + 12, self.y - 2, self.x + 26 + 12, self.y + 62 - 2]
        elif self.active_move["Right"]:
            cords = [self.x + 22, self.y + 48, self.x + 22 + 26, self.y + 48 + 12]
            # cords = [self.x + 22, self.y - 2, self.x + 26 + 22, self.y + 62 - 2]
        elif self.active_move["Back"]:
            cords = [self.x + 16, self.y + 42, self.x + 16 + 20, self.y + 42 + 10]

        else:
            cords = [self.x + 16, self.y + 52, self.x + 16 + 20, self.y + 52 + 10]
        return cords

    def moving(self, player_cords=None):

        cords = self.get_collision_box()

        col1, col2 = (cords[0]) // 32, (cords[2]) // 32
        row1, row2 = (cords[1]) // 32, (cords[3]) // 32

        if self.status == "friendly":

            if self.move_choise == "Forward" and self.chek_collisions(col1, row1, col2, row2):
                self.y += MONSTER_SPEED

            elif self.move_choise == "Back" and self.chek_collisions(col1, row1, col2, row2):
                self.y -= MONSTER_SPEED

            elif self.move_choise == "Right" and self.chek_collisions(col1, row1, col2, row2):
                self.x += MONSTER_SPEED

            elif self.move_choise == "Left" and self.chek_collisions(col1, row1, col2, row2):
                self.x -= MONSTER_SPEED

            # self.chek_active_move(self.move_choise)

        elif self.status == "aggressive":

            if self.y < player_cords[1] - MONSTER_SPEED + 20 and self.chek_collisions(col1, row1, col2, row2):
                self.y += MONSTER_SPEED
                self.move_choise = "Forward"

            elif self.y > player_cords[1] + 20 and self.chek_collisions(col1, row1, col2, row2):
                self.y -= MONSTER_SPEED
                self.move_choise = "Back"

            elif self.x < player_cords[0] - MONSTER_SPEED + 15 and self.chek_collisions(col1, row1, col2, row2):
                self.x += MONSTER_SPEED
                self.move_choise = "Right"

            elif self.x > player_cords[0] + 15 and self.chek_collisions(col1, row1, col2, row2):
                self.x -= MONSTER_SPEED
                self.move_choise = "Left"
