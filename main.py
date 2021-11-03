import pygame, sys
from pygame.locals import *
import numpy as np

''' clock '''
clock = pygame.time.Clock()

# initiates pygame
pygame.init()

# initiate window
window_size = (600, 400)  # PREVIOUSLY: (1280, 720)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Wilt-Blizzard Quest")
display = pygame.Surface((300, 200))

''' load assets '''
# Background
bg_image = pygame.image.load(r'.\Assets\backgrounds\background3-720.png')
# Player
player_image = pygame.image.load(r'.\Assets\player-small.png')
# set transparent color key: otherwise the player image will have a white border when on top of another surface
# player_image.set_colorkey((255, 255, 255))

# Tiles
grass_image = pygame.image.load(r'.\Assets\tiles\dryGrass-01.png')
ice_image = pygame.image.load(r'.\Assets\tiles\thickIce-01.png')
dirt_image = pygame.image.load(r'.\Assets\tiles\dirt-01.png')

tile_size = dirt_image.get_width()

# Map
# game_map = np.zeros(shape=(90,160)) # generate RowxCol by dividing dims of bg_img with pixel sz of tiles
# game_map[45] = 2
# game_map[46:] = 1
# game_map_terrain = np.zeros(shape=(20, 160)) + 3
# game_map[24:44] = game_map_terrain

game_map = [
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2'],
    ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
]

"""Physics"""


def collision_test(rect, tiles):
    # rect is the player
    # tiles are map tiles
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    # rect is the rect of the player
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        # right collisions
        if movement[0] > 0:
            # player on left sets its right side equal to the left side of the tile it collides with
            rect.right = tile.left
            collision_types['right'] = True
        # left collisions
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    # update y position
    rect.y += movement[1]
    # check for collision again because we are now in a different collision from before because of what we did with the x axis
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        # bottom collision
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        # top collisions
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


moving_right = False
moving_left = False
jump = False

player_y_momentum = 0
air_timer = 0

# player rect for collisions
player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

''' game loop '''
while True:
    display.blit(bg_image, (0, 0))

    # game map rendering
    tile_rect = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * tile_size, y * tile_size))
            if tile == '2':
                display.blit(ice_image, (x * tile_size, y * tile_size))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1

    # player movement
    # NOTE: this is not the position of player but how much we intend to move the player (Velocity)
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2

    # Gravity
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    # set limit on fall velocity
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rect)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum = 0

    # player image
    display.blit(player_image, (player_rect.x, player_rect.y))

    # Player inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    """ Upkeep """
    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0, 0))
    # update screen
    pygame.display.update()
    # sets game to 60 fps
    clock.tick(60)
    current_time = pygame.time.get_ticks()
