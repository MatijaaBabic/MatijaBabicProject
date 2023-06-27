import pygame
import sys
import random
import os
from pygame import mixer
import pygame_menu
import math

os.chdir(r"C:\Users\Windows 10\Desktop\Microsoft\Prezentacije\Programs for school\Code\Github\MatijaBabicProject\Project Code\Prototypes\Prototype May 2023\Prototype Assets")  # The working path of this prototype, where the assets are located

# Basic colors defined here
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (115, 181, 239)
YELLOW = (234, 226, 61)
CYAN = (0, 100, 100)

# Defining important classes
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
        self.current_frame = 0
        self.animation_timer = 0
        self.rotation = [
            pygame.image.load("pup.png"),
            pygame.image.load("pleft.png"),
            pygame.image.load("pdown.png"),
        ]
        # Array that stores pictures for the character turning
        self.movement = [
            [
                pygame.image.load("walkup1.png"),
                pygame.image.load("walkup2.png"),
                pygame.image.load("walkup3.png"),
            ],
            [
                pygame.image.load("walkleft1.png"),
                pygame.image.load("walkleft2.png"),
                pygame.image.load("walkleft3.png"),
            ],
            [
                pygame.image.load("walkdown1.png"),
                pygame.image.load("walkdown2.png"),
                pygame.image.load("walkdown3.png"),
            ],
        ]  # Array that stores images for animating the movement
        self.speed = 5

    def move(self):
        control = pygame.key.get_pressed()
        if control[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.right = False
            self.left = True
            self.up = False
            self.down = False
            self.turn()
            self.animate_movement(1)  # Start walking animation in the "left" direction
        if control[pygame.K_d] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.turn()
            self.animate_movement(1)  # Start walking animation in the "right" direction
        if control[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.turn()
            self.animate_movement(0)  # Start walking animation in the "up" direction
        if control[pygame.K_s] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.turn()
            self.animate_movement(2)  # Start walking animation in the "down" direction

    def turn(self):
        if self.up:
            self.image = self.rotation[0]
            self.orientation = "up"
        if self.left:
            self.image = self.rotation[1]
            self.orientation = "left"
        if self.down:
            self.image = self.rotation[2]
            self.orientation = "down"

    def animate_movement(self, direction):
        if self.animation_timer < 10:
            self.animation_timer += 1
        else:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame > 2:
                self.current_frame = 0
        self.image = self.movement[direction][self.current_frame]

    def update_projectiles(self):
        self.bullet.update()

    def shoot(self):
        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            self.orientation,
        )
        self.bullet.add(bullet)

    def get_teleport_direction(self):
        if self.up and self.left:
            return "upleft"
        elif self.up and self.right:
            return "upright"
        elif self.down and self.left:
            return "downleft"
        elif self.down and self.right:
            return "downright"
        elif self.up:
            return "up"
        elif self.down:
            return "down"
        elif self.left:
            return "left"
        elif self.right:
            return "right"

    def get_teleport_destination(self):
        if self.teleport_direction == "upleft":
            dest_x = self.rect.x - self.teleport_distance
            dest_y = self.rect.y - self.teleport_distance
        elif self.teleport_direction == "upright":
            dest_x = self.rect.x + self.teleport_distance
            dest_y = self.rect.y - self.teleport_distance
        elif self.teleport_direction == "downleft":
            dest_x = self.rect.x - self.teleport_distance
            dest_y = self.rect.y + self.teleport_distance
        elif self.teleport_direction == "downright":
            dest_x = self.rect.x + self.teleport_distance
            dest_y = self.rect.y + self.teleport_distance
        elif self.teleport_direction == "up":
            dest_x = self.rect.x
            dest_y = self.rect.y - self.teleport_distance
        elif self.teleport_direction == "down":
            dest_x = self.rect.x
            dest_y = self.rect.y + self.teleport_distance
        elif self.teleport_direction == "left":
            dest_x = self.rect.x - self.teleport_distance
            dest_y = self.rect.y
        elif self.teleport_direction == "right":
            dest_x = self.rect.x + self.teleport_distance
            dest_y = self.rect.y

        # Ensure the destination is within the screen bounds
        dest_x = max(0, min(dest_x, self.screen_width - self.rect.width))
        dest_y = max(0, min(dest_y, self.screen_height - self.rect.height))

        return dest_x, dest_y

    def update(self):
        if self.is_teleporting:
            self.teleport_timer += 1
            if self.teleport_timer >= self.teleport_cooldown:
                self.is_teleporting = False
                self.teleport_timer = 0
        else:
            self.move()
            if self.teleport_timer != 0:
                self.teleport_timer = 0

        if pygame.mouse.get_pressed()[0] and not self.is_teleporting:
            self.shoot()

        self.update_projectiles()
        self.bullet.draw(screen)
        self.bullet.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if (
            self.rect.y < -10
            or self.rect.y > screen_height + 10
            or self.rect.x < -10
            or self.rect.x > screen_width + 10
        ):
            self.kill()


# Initialize pygame
pygame.init()

# Set the width and height of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("My Game")

# Create the player object
player = Player(50, 50, screen_width, screen_height)

# Create all the sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
running = True
while running:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Game logic
    all_sprites.update()

    # --- Drawing code
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # --- Update the screen
    pygame.display.flip()

    # --- Limit frames per second
    clock.tick(60)

# Close the window and quit
pygame.quit()
sys.exit()

