import pygame
import sys
import random
import os
from pygame import mixer
import pygame_menu
import math
import methods
os.chdir(r"C:\Users\Windows 10\Desktop\Microsoft\Prezentacije\Programs for school\Code\Github\MatijaBabicProject\Project Code\Prototypes\Prototype May 2023\Prototype Assets") #the working path of this prototype, where the assets are located
# Basic colors defined here
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (115, 181, 239)
YELLOW = (234, 226, 61)
CYAN = (0, 100, 100)

pygame.init()
info = pygame.display.Info()
SIZE = W, H = info.current_w, info.current_h
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Steel Gear Liquid")
player = methods.Player(960, 540, W, H)
done = True

clock = pygame.time.Clock()

while done:
    screen.fill(CYAN)   #for demonstration purposes
    #screen.fill(BLACK) #for actual use in game
    player.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                player.shoot()
    player.move()
    player.update_projectiles()
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
