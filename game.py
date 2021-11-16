import pygame
from menu import *
# Image
snake_image = pygame.image.load('graphics/snake_head.png')
# Set window
w_height = 720
w_width = 480
screen = pygame.display.set_mode((w_width, w_height))


class Game():
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

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Game Over", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

# Player
class Snake:

    def init(self):
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
