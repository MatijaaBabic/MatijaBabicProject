import pygame
import sys
import random
import os
from pygame import mixer
import pygame_menu
os.chdir(r"C:\Users\Windows 10\Desktop\Microsoft\Prezentacije\Programs for school\Code\Github\MatijaBabicProject\Project Code\Prototypes\Prototype May 2023\Prototype Assets") #the working path of this prototype, where the assets are located
# Basic colors defined here
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (115, 181, 239)
YELLOW = (234, 226, 61)
CYAN = (0, 100, 100)
#defining important classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("pdown.png")
        self.health = 100
        self.right = False
        self.left = False
        self.up = False
        self.down = True
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
        self.screen_width = screen_width
        self.screen_height = screen_height      
        self.rotation = [
            pygame.image.load("pup.png"),
            pygame.image.load("pleft.png"),
            pygame.image.load("pdown.png")
        ]
        #array that stores pictures for the character turning
        self.movement = [

        ] #array that stores images for animating the movement
        self.speed = 10
    
    def move(self):
        control = pygame.key.get_pressed()
        if control[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.right = False
            self.left = True
            self.up = False
            self.down = False
            self.turn()
        if control[pygame.K_d] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.turn()
        if control[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.turn()
        if control[pygame.K_s] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.turn()
        if control[pygame.K_a] and control[pygame.K_w] and self.rect.left > 0 and self.rect.top > 0:
            self.rect.x -= (self.speed - 7)
            self.rect.y -= (self.speed - 7)
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.turn()
        if control[pygame.K_a] and control[pygame.K_s] and self.rect.left > 0 and self.rect.bottom < self.screen_height:
            self.rect.x -= (self.speed - 7)
            self.rect.y += (self.speed - 7)
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.turn()
        if control[pygame.K_d] and control[pygame.K_w] and self.rect.right < self.screen_width and self.rect.top > 0:
            self.rect.x += (self.speed - 7)
            self.rect.y -= (self.speed - 7)
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.turn()
        if control[pygame.K_d] and control[pygame.K_s] and self.rect.right < self.screen_width and self.rect.bottom < self.screen_height:
            self.rect.x += (self.speed - 7)
            self.rect.y += (self.speed - 7)
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.turn()
    def turn(self):
        if self.up == True:
            self.image = self.rotation[0]
        if self.down == True:
            self.image = self.rotation[2]
        if self.left == True:
            self.image = self.rotation[1]
        if self.right == True:
            self.image = pygame.transform.flip(self.rotation[1], True, False) #instead of using a different sprite, I will just flip the left one
    def draw(self, screen):
        screen.blit(self.image, self.rect)

pygame.init()
info = pygame.display.Info()
SIZE = W, H = info.current_w, info.current_h
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Steel Gear Liquid")
player = Player(960, 540, W, H)
done = True

clock = pygame.time.Clock()

while done:
    screen.fill(CYAN)
    player.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    player.move()
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
