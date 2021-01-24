from Constants import *
import pygame


class Mob:
    def __init__(self, screen, image_pack):
        self.screen = screen
        self.image_pack = image_pack

        self.health_point = HP

        self.moves = []

        self.x = 500
        self.y = 200

        image = pygame.image.load(self.image_pack[0]).convert_alpha()

        pose = pygame.transform.scale(image.subsurface(43, 0, 49, 69), (50, 70))
        self.moves.append(pose)

    # def filling_moves(self):
    #     for link in self.image_pack:
    #         image = pygame.image.load(link).convert_alpha()
    #
    #         pose1 = pygame.transform.scale(image.subsurface(0, 0, 49, 69), (50, 70))
    #
    #         pose2 = pygame.transform.scale(image.subsurface(43, 0, 49, 69), (50, 70))
    #
    #         pose3 = pygame.transform.scale(image.subsurface(103, 0, 49, 69), (50, 70))
    #
    #         self.moves.append([pose1,
    #                            pose2,
    #                            pose3,
    #                            pose2])

    def render(self):
        self.screen.blit(self.moves[0], (self.x, self.y))


class Crocodile(Mob):
    def __init__(self, screen):
        self.screen = screen
        self.image_pack = ["Resources/crocodile_go.png", "Resources/crocodile_go_back.png",
                           "Resources/crocodile_go_right.png", "Resources/crocodile_go_left.png"]
        Mob.__init__(self, self.screen, self.image_pack)
