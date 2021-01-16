from Constants import *
import pygame


class Hero:
    def __init__(self, screen):

        self.screen = screen

        self.health_point = HP

        self.moves = []
        self.active_move = {"Forward": False, "Back": False, "Right": False, "Left": False}
        self.animation_counter = 0

        self.x = 50
        self.y = 50

    def filling_moves(self):
        images = ["Resoources1/go.png", "Resoources1/go_back.png",
                  "Resoources1/go_right.png", "Resoources1/go_left.png"]

        for link in images:
            image = pygame.image.load(link).convert_alpha()
            self.moves.append([image.subsurface(0, 0, 17, 28),
                               image.subsurface(24, 0, 17, 28),
                               image.subsurface(47, 0, 17, 28)])

    def render(self):
        active_key = 0

        if self.animation_counter + 1 >= 15:
            self.animation_counter = 0

        if self.active_move["Forward"]:
            self.screen.blit(self.moves[0][self.animation_counter // 5])
            active_key = 0

        elif self.active_move["Back"]:
            self.screen.blit(self.moves[1][self.animation_counter // 5])
            active_key = 1

        elif self.active_move["Right"]:
            self.screen.blit(self.moves[2][self.animation_counter // 5])
            active_key = 2

        elif self.active_move["Left"]:
            self.screen.blit(self.moves[3][self.animation_counter // 5])
            active_key = 3

        else:
            self.screen.blit(self.moves[active_key][1])

        self.animation_counter += 1

    def chek_active_move(self, skip_key):
        for key in self.active_move.keys():
            if key != skip_key:
                self.active_move[key] = False

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
            self.active_move["Forward"] = True
            self.y += SPEED
            skip_key = "Forward"

        self.chek_active_move(skip_key)
