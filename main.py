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
bg_image = pygame.transform.scale(bg_image, (300, 200))
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
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map(r'Assets\map')

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
true_scroll = [0, 0]

# player rect for collisions
player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

# [[scale, [x_position, y_position, width, height]], ... ]
background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                      [0.5, [130, 90, 100, 400]], [0.75, [300, 80, 120, 400]]]

''' game loop '''
while True:
    display.blit(bg_image, (0, 0))

    # the content in the () locates the camera on the player
    # Dividing this by 20 creates the camera lag effect
    # this occurs because in () is the difference between the player location and the camera location
    # therefore dividing this amount will

    # Additionally a copy of the scroll value is made and applied on the tiles movement to be integer values
    #  the reason for this is because if decimals are used there is an effect where the tiles will slide into each other
    true_scroll[0] += (player_rect.x - true_scroll[0] - 153) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # game map rendering
    pygame.draw.rect(display, (13, 13, 20), pygame.Rect(0, 120, 300, 80))
    for background_object in background_objects:
        # first two arguments are the position and move the
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0]*background_object[0],
                             background_object[1][1] - scroll[1] * background_object[0],
                             background_object[1][2],
                             background_object[1][3]
                             )
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (50, 88, 168), obj_rect)
        elif background_object[0] == 0.75:
            pygame.draw.rect(display, (52, 51, 94), obj_rect)
        else:
            pygame.draw.rect(display, (50, 119, 168), obj_rect)

    tile_rect = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '2':
                display.blit(ice_image, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
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
    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

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
