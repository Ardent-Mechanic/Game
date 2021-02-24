SCREEN_HEIGHT = 1024
SCREEN_WEIGHT = 1024

HP = 243
MANA = 243

HP_REGEN = 1
MN_REGEN = 1

SPEED = 5
FPS = 60

MONSTER_SPEED = 3
MONSTER_HP = 50
MONSTER_LINE_OF_SIGHT = 150

MONSTER_HITBOX_HEIGHT = 30
MONSTER_HITBOX_WEIGHT = 30

HEALTH_BAR_CORDS = (775, 5, 249, 29)
MANA_BAR_CORDS = (775, 30, 249, 29)

PLAYER_HITBOX_HEIGHT = 34 * 2
PLAYER_HITBOX_WEIGHT = 28 * 2

PLAYER_SIZE = (28 * 2, 34 * 2)
MONSTER_SIZE = (32, 32)
# PLAYER_SIZE = (28, 34)

MAX_FRAMES_FOR_IMAGE = 4

LVL = [{"PLAYER_CORD": [100, 100],
       "MONSTERS": [["snake", [250, 100]], ["fire", [450, 240]], ["snake", [96, 896]], ["snake", [448, 640]]]},
       {"PLAYER_CORD": [100, 100],
        "MONSTERS": [["snake", [400, 200]], ["fire", [768, 432]],
                     ["snake", [120, 896]], ["snake", [448, 640]], ["fire", [256, 576]]]}
       ]
LVL_MONSTER = [["snake", "fire", "snake", "snake"], ["fire", "fire", "fire", "snake"]]
