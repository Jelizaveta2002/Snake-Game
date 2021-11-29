import random
import pygame
import sys
from pygame.math import Vector2

import game_over
from game_over import *
from menu import *

# initiate pygame
pygame.init()

# Game name
pygame.display.set_caption('Snake')

# initiate pygame
pygame.init()

# Set window
w_height = 720
w_width = 480
screen = pygame.display.set_mode((w_width, w_height))

# Game name
pygame.display.set_caption('Runner')

# Image
snake_image = pygame.image.load('graphics/snake_head.png')
snake_body_image = pygame.image.load('graphics/snake_body.png')
apple_image = pygame.image.load('graphics/apple.png')


start_img = pygame.image.load("graphics/apple.png").convert_alpha()
exit_img = pygame.image.load("graphics/apple.png").convert_alpha()

# Blocks
block_image = pygame.image.load('graphics/block.png')
SPAWNBLOCK = pygame.USEREVENT
pygame.time.set_timer(SPAWNBLOCK, 1200)
break_block = pygame.image.load('graphics/breakable_block.png')
space_image = pygame.image.load('graphics/space.png')

import time
clock = pygame.time.Clock()


class Game:

    def __init__(self):
        pygame.init()
        self.running, self.playing, self.game_over_screen = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RUN_KEY, self.EXIT_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (145, 254, 222), (215, 100, 91)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.game_over = GameOverMain(self)
        self.curr_game_over = self.game_over
        self.eaten_apples = 0
        self.list_of_apples = []
        self.BLOCK_list = []

    def crash(self):
        file = 'music/game_over.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(1)
        self.playing = False
        self.game_over_screen = True

    def create_block(self):
        res = []

        while len(res) != 9:
            num = [1, 2, 3]
            class_num = random.choice(num)
            if len(res) == 4:
                add_space = True
                for val in res:
                    if type(val) == Space:
                        add_space = False
                if add_space:
                    res.append(Space())
                    print('space')
            if class_num == 1:
                res.append(Block())
            elif class_num == 2:
                res.append(BreakableBlock())
            elif class_num == 3:
                res.append(Space())

        total_l = 0
        for elem in range(9):
            res[elem].rect.left = total_l
            total_l += 54

        return res

    def move_block(self, block_list):
        for block in block_list:
            for each in block:
                each.update()

    def draw_block(self, block_list):
        for block in block_list:
            for each in block:
                each.draw()

    def remove_block(self, block_list):
        for block in self.BLOCK_list:
            if block[0].rect.y > w_height:
                self.BLOCK_list.remove(block)

    def check_crash(self, snake):
        for block in self.BLOCK_list:
            for elem in block:
                collision_tolerance = 10
                if snake.rect.colliderect(elem.rect):
                    if abs(elem.rect.bottom - snake.rect.top) < collision_tolerance:
                        if type(elem) == BreakableBlock:
                            print('-apple')
                            elem.respawn()
                            self.list_of_apples = self.list_of_apples[:-1]
                            self.eaten_apples -= 1
                            # for x in self.list_of_apples:
                            #     new_variable = snake.rect_body.y + 26 * x
                            #     screen.blit(snake.image_body, (snake.rect_body.x, new_variable))
                            if self.eaten_apples < 0:
                                self.crash()
                        elif type(elem) == Block:
                            self.crash()
                            self.playing = False
                    if abs(elem.rect.right - snake.rect.left) < collision_tolerance:
                        snake.rect.left = elem.rect.right + 1
                        # print('left')
                    if abs(elem.rect.left - snake.rect.right) < collision_tolerance:
                        snake.rect.right = elem.rect.left - 1
                        # print('right')
                    if abs(elem.rect.right - snake.rect_body.left) < collision_tolerance:
                        snake.rect_body.left = elem.rect.right + 1
                    if abs(elem.rect.left - snake.rect_body.right) < collision_tolerance:
                        snake.rect_body.right = elem.rect.left - 1

    def game_loop(self):
        self.eaten_apples = 0
        self.list_of_apples = []
        snake = Snake()
        # block = Block()
        apple = Apple()
        breakable_block = BreakableBlock()
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

            # Movement
            snake.update()
            self.check_crash(snake)
            apple.update()
            breakable_block.update()

            # On screen
            screen.fill('#ccffcc')
            screen.blit(snake.image, (snake.rect.x, snake.rect.y))
            screen.blit(apple.image, (apple.rect.x, apple.rect.y))

            # Blocks
            self.move_block(self.BLOCK_list)
            self.draw_block(self.BLOCK_list)
            self.remove_block(self.BLOCK_list)

            if self.eaten_apples > -1:
                for x in self.list_of_apples:
                    new_variable = snake.rect_body.y + 26 * x
                    screen.blit(snake.image_body, (snake.rect_body.x, new_variable))

            if snake.rect.colliderect(apple.rect):
                self.eaten_apples += 1
                self.list_of_apples.append(self.eaten_apples)
                apple.respawn()
                print(self.eaten_apples)

            pygame.display.update()
            clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if self.game_over_screen:
                    if event.key == pygame.K_RETURN:
                        self.RUN_KEY = True
                        self.START_KEY = False
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.EXIT_KEY = True
                    self.curr_menu.run_display = False
                    self.curr_game_over.run_display = False
                    self.running, self.playing = False, False
                    quit()
                    pygame.quit()
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == SPAWNBLOCK and self.playing == True:
                self.BLOCK_list.append(self.create_block())
                print(self.BLOCK_list)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RUN_KEY = False, False, False, False, False


class Snake:

    def __init__(self):
        self.image = snake_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = int(w_width * 0.5)
        self.rect.y = int(w_height * 0.5)

        self.image_body = snake_body_image
        self.width_body = self.image_body.get_width()
        self.height_body = self.image_body.get_height()

        self.rect_body = self.image_body.get_rect()
        self.rect_body.x = int(w_width * 0.5)
        self.rect_body.y = int(w_height * 0.5)

        self.speed_x = 10

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= 5
            self.rect_body.x -= 5
        if key_state[pygame.K_RIGHT]:
            self.rect.x += 5
            self.rect_body.x += 5

        # Check boundary
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.left > east_b:
            self.rect.left = east_b
        if self.rect_body.left < west_b:
            self.rect_body.left = west_b
        if self.rect_body.left > east_b:
            self.rect_body.left = east_b


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
        self.rect.x = 5
        self.rect.y = -100

        self.speedy = 5

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y = self.rect.y + self.speedy


class Space:
    def __init__(self):
        self.image = space_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = -100

        self.speedy = 5

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y = self.rect.y + self.speedy


class BreakableBlock:
    def __init__(self):
        self.image = break_block
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = -100

        self.speedy = 5

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y = self.rect.y + self.speedy

    def respawn(self):
        self.rect.x = random.randrange(west_b, east_b - self.width) + 1000


# Apples
class Apple:
    def __init__(self):
        self.image = apple_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(west_b, east_b)
        self.rect.y = 200

        self.speedy = 6

    def update(self):
        self.rect.y = self.rect.y + self.speedy

        # Check boundary of an Apple
        if self.rect.y > w_height:
            self.rect.y = 0 - self.height
            self.rect.x = random.randrange(west_b, east_b - self.width)

    def respawn(self):
        self.rect.x = random.randrange(west_b, east_b - self.width) + 1000
