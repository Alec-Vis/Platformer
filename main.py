import pygame, sys
from pygame.locals import *

''' clock '''
clock = pygame.time.Clock()

# initiates pygame
pygame.init()

# initiate window
window_size = (1280,720)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Wilt-Blizzard Quest")

''' load assets '''
# Background
bg_image = pygame.image.load(r'.\Assets\backgrounds\background3-720.png')
# Player
player_image = pygame.image.load(r'.\Assets\player-small.png')

moving_right = False
moving_left = False
jump = False

player_location = [50,50]
player_y_momentum = 0

# player rect for collisions
player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

''' game loop '''
while True:
    screen.blit(bg_image, (0,0))
    # player image
    screen.blit(player_image, player_location)
    #  gravity
    if player_location[1] > window_size[1] - player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2

    player_location[1] += player_y_momentum

    # player movement
    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    # rect follows player, the alternative is to redefine the rect variable
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255, 200,0), test_rect)
    else:
        pygame.draw.rect(screen, (0,200,255), test_rect)

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
                jump = True
                jump_time = current_time + 360
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False


    # update screen
    pygame.display.update()
    # sets game to 60 fps
    clock.tick(60)
    current_time = pygame.time.get_ticks()