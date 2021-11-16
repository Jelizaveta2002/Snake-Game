import random
import pygame
import sys

from menu import *


# initiate pygame
pygame.init()

# Set window
w_height = 720
w_width = 480
screen = pygame.display.set_mode((w_width, w_height))

# Game name
pygame.display.set_caption('Runner')

# image
# bg=pygame.image.load()
snake_image = pygame.image.load('graphics/snake_head.png')
block_image = pygame.image.load('graphics/block.png')

import time
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (145, 254, 222), (215, 100, 91)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    # Game functions
    def crash(self):
        self.display.fill(self.BLACK)
        self.draw_text("Game Over", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        time.sleep(2)
        self.game_loop()

    def game_loop(self):

        snake = Snake()
        block = Block()
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

            # Movement
            snake.update()
            block.update()

            # On screen
            screen.fill('#ccffcc')
            screen.blit(snake.image, (snake.rect.x, snake.rect.y))
            screen.blit(block.image, (block.rect.x, block.rect.y))

            collision_tolerance = 10
            if snake.rect.colliderect(block.rect):
                if abs(block.rect.bottom - snake.rect.top) < collision_tolerance:
                    self.crash()
                if abs(block.rect.right - snake.rect.left) < collision_tolerance:
                    snake.rect.left = block.rect.right + 1
                    print('left')
                if abs(block.rect.left - snake.rect.right) < collision_tolerance:
                    snake.rect.right = block.rect.left - 1
                    print('right')

            pygame.display.update()
            clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
#

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
#


class Snake:

    def __init__(self):
        self.image = snake_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = int(w_width * 0.5)
        self.rect.y = int(w_height * 0.5)

        self.speed_x = 10

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= 7
        if key_state[pygame.K_RIGHT]:
            self.rect.x += 7

        # Check boundary
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.left > east_b:
            self.rect.left = east_b


# Boundary
west_b = 0
east_b = 448


# Blocks
class Block:
    def __init__(self):
        self.image = block_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(west_b, east_b)
        self.rect.y = 100

        self.speedy = 5

    def update(self):
        self.rect.y = self.rect.y + self.speedy

        # Check boundary of block
        if self.rect.y > w_height:
            self.rect.y = 0 - self.height
            self.rect.x = random.randrange(west_b, east_b - self.width)
