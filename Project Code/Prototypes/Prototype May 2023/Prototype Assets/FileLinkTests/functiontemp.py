import pygame
import sys
import random
import os
from pygame import mixer
import pygame_menu
import math
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
        self.bullet = pygame.sprite.Group() 
        self.orientation = "down" 
        self.teleport_distance = 50
        self.teleport_cooldown = 10
        self.teleport_timer = 0
        self.is_teleporting = False
        self.teleport_direction = None
        self.teleport_destination = None
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
        if control[pygame.K_LSHIFT] and not self.is_teleporting and self.teleport_timer <= 0:
            self.is_teleporting = True
            self.teleport_direction = self.get_teleport_direction()
            self.teleport_destination = self.get_teleport_destination()

        if self.is_teleporting:
            self.perform_teleport()

        if self.teleport_timer > 0:
            self.teleport_timer -= 1
    
    def turn(self):
        if self.up == True:
            self.image = self.rotation[0]
            self.orientation = "up"
        if self.down == True:
            self.image = self.rotation[2]
            self.orientation = "down"
        if self.left == True:
            self.image = self.rotation[1]
            self.orientation = "left"
        if self.right == True:
            self.image = pygame.transform.flip(self.rotation[1], True, False) #instead of using a different sprite, I will just flip the left one
            self.orientation = "right"
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullet.draw(screen)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, (self.rect.top + 15), self.orientation)
        self.bullet.add(bullet)

    def update_projectiles(self):
        self.bullet.update()
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
    def get_teleport_direction(self):
        direction = [0, 0]
        control = pygame.key.get_pressed()
        if control[pygame.K_a]:
            direction[0] -= 1
        if control[pygame.K_d]:
            direction[0] += 1
        if control[pygame.K_w]:
            direction[1] -= 1
        if control[pygame.K_s]:
            direction[1] += 1

        return direction

    def get_teleport_destination(self):
        dest_x = self.rect.x + self.teleport_direction[0] * self.teleport_distance
        dest_y = self.rect.y + self.teleport_direction[1] * self.teleport_distance
        dest_x = max(0, min(dest_x, self.screen_width)) #creates boundaries for what can the destination of a teleport be, preventing teleporting out of bounds
        dest_y = max(0, min(dest_y, self.screen_height))
        return dest_x, dest_y

    def perform_teleport(self):
        self.rect.x, self.rect.y = self.teleport_destination
        self.is_teleporting = False
        self.teleport_timer = self.teleport_cooldown




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 15
        self.orientation = orientation

    
    def update(self):
        if self.orientation == "up":
            self.rect.y -= self.speed
        elif self.orientation == "down":
            self.rect.y += self.speed
        elif self.orientation == "left":
            self.rect.x -= self.speed
        elif self.orientation == "right":
            self.rect.x += self.speed

