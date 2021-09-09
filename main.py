import pygame, sys
from pygame.locals import *

''' clock '''
clock = pygame.time.Clock()

# initiates pygame
pygame.init()

# initiate window
window_size = (1000,800)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Wilt-Blizzard Dynasty")

''' game loop '''
while True:

    # key board events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    # sets game to 60 fps
    clock.tick(60)