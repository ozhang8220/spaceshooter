# Import the pygame module
import pygame
import random
import math
import sys

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# color
WHITE = (255, 255, 255)

font_name = pygame.font.match_font('arial')
# draws the text on the screen 
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player():
    def __init__(self):
        self.image = pygame.image.load('character.png')
        # rectangle for sprite
        DEFAULT_IMAGE_SIZE = (150, 100)
        # Scale the image 
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

    def movement(self):
        key = pygame.key.get_pressed()
        distance = 5
        if key[K_s]: # down key
            if self.y <= (SCREEN_HEIGHT - 100):
                self.y += distance # move down
        elif key[K_w]: # up key
            if self.y != 0:
                self.y -= distance # move up
        if key[K_d]: # right key
            if self.x <= (SCREEN_WIDTH - 150):
                self.x += distance # move right
        elif key[K_a]: # left key
            if self.x != 0:
                self.x -= distance # move left'd
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
    
    def get_rectangle(self):
        return self.rect
    
class Enemy():
    def __init__(self):
        self.image = pygame.image.load('enemy.png')
        # rectangle for sprite
        DEFAULT_IMAGE_SIZE = (30, 30)
        # Scale the image 
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        enemy_x = player.x + 75
        enemy_y = player.y + 50
        while abs(enemy_x - player.x + 75) <= 150:
            enemy_x = random.randint(0, SCREEN_WIDTH)
        while abs(enemy_y - player.y + 50) <= 100:
            enemy_y = random.randint(0, SCREEN_HEIGHT)

        self.x = enemy_x
        self.y = enemy_y
        
    def movement(self):
        mx = player.x + 75
        my = player.y + 50
        self.dir = (mx - self.x, my - self.y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.speed = 1
        self.x = self.x + self.dir[0] * self.speed
        self.y = self.y + self.dir[1] * self.speed
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rectangle(self):
        return self.rect
    


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Bullet():
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 5)).convert_alpha()
        self.bullet.fill((0, 0, 0))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 4

    def update(self):  
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)
        self.rect = self.bullet.get_rect(center = self.pos)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)

    def get_rectangle(self):
        return self.rect

# game over screen 
def show_go_screen():
    screen.blit(bg, bg_rect)
    draw_text(screen, "SASSY SHOOTAS", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "WASD move, Click mouse to fire", 22, SCREEN_WIDTH  / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "3 lives, 1 mission: Survive", 22, SCREEN_WIDTH  / 2, SCREEN_HEIGHT / 2 + 25)
    draw_text(screen, "Press a key to begin", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()

    waiting = True 
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP: 
                waiting = False


# Instantiate player
player = Player()

bullets = []
enemies = []

SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY, 1000)


# set screen size
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# set variable bg for background
bg = pygame.image.load("bg.png")
bg_rect = bg.get_rect()
bg = pygame.transform.scale(bg,(SCREEN_WIDTH,SCREEN_HEIGHT))

# set variable bg2 for end background
bg2 = pygame.image.load("steve.png")
bg2 = pygame.transform.scale(bg2,(SCREEN_WIDTH,SCREEN_HEIGHT))




# Variable to keep the main loop running
running = True
# variable to set to game_over 
game_over = True
score = 0
lives = 3

# Main loop
while running:

    # start game_over actions 
    if game_over:
        show_go_screen()
        game_over = False 

        # resets all the values/variables
        player = Player()
        bullets = []
        enemies = []
        score = 0

    clock.tick(60)
    # for loop through the event queue
    for event in pygame.event.get():
        # If the Esc key is pressed, then exit the main loop
        if event.type == QUIT:
            pygame.quit()
            running = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(Bullet(player.x + 75, player.y + 50))
        if event.type == SPAWNENEMY:
            enemies.append(Enemy())
    
    player.movement()

    for bullet in bullets[:]:
        bullet.update()
        if not screen.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy.movement()
        enemy_rectangle = enemy.get_rectangle()
        player_rectangle = player.get_rectangle()
        if player_rectangle.colliderect(enemy_rectangle):
            enemies.remove(enemy)
            lives = lives - 1
    
    if lives == 0:
        game_over = True

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            enemy_rectangle = enemy.get_rectangle()
            bullet_rectangle = bullet.get_rectangle()
            if bullet_rectangle.colliderect(enemy_rectangle):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

    # put background in
    screen.blit(bg,(0,0))

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
        
    for enemy in enemies:
        enemy.draw(screen)
    
    draw_text(screen, "Score: " + str(score), 18, SCREEN_WIDTH / 2, 10)

    # Update the display
    pygame.display.update()
