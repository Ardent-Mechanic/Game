from Constants import *
import pygame


class Hero:
    def __init__(self):
        self.health_point = HP
        self.moves = []
        self.x = 50
        self.y = 50

    def filling_moves(self):
        images = ["Resoources1/go.png", "Resoources1/go_back.png",
                  "Resoources1/go_right.png", "Resoources1/go_left.png"]
        for link in images:
            image = pygame.image.load(link).convert_alpha()
            self.moves.append([image.subsurface(0, 0, 17, 28),
                               image.subsurface(24, 0, 17, 28),
                               image.subsurface(48, 0, 16, 28)])



