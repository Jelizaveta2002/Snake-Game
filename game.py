import random
from menu import *
import pygame as pg
# initiate pygame
pygame.init()

# Game name
pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load('graphics/snake_head.png'))

# initiate pygame
pygame.init()

# Set window
w_height = 720
w_width = 480
screen = pygame.display.set_mode((w_width, w_height))


# Image
snake_image = pygame.image.load('graphics/snake_head.png')
snake_body_image = pygame.image.load('graphics/snake_body.png')
apple_image = pygame.image.load('graphics/apple.png')
bullet_image = pygame.image.load('graphics/bullet.png')

start_img = pygame.image.load("graphics/apple.png").convert_alpha()
exit_img = pygame.image.load("graphics/apple.png").convert_alpha()

# Blocks
block_image = pygame.image.load('graphics/block.png')
SPAWNBLOCK = pygame.USEREVENT
pygame.time.set_timer(SPAWNBLOCK, 1200)
break_block = pygame.image.load('graphics/breakable_block.png')
space_image = pygame.image.load('graphics/space.png')

clock = pygame.time.Clock()


font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


class Game:
    def __init__(self):
        self.music_play = True
        self.start = False
        self.change = False
        pygame.init()
        self.running, self.playing, self.game_over_screen = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.EXIT_KEY = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "font/8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (145, 254, 222), (215, 100, 91)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.instruction = InstructionMenu(self)
        self.curr_menu = self.main_menu
        self.game_over = GameOverMenu(self)
        self.pause = PauseMenu(self)
        self.curr_game_over = self.game_over
        self.eaten_apples = 0
        self.list_of_apples = []
        self.BLOCK_list = []
        self.paused = False
        self.g_over = False
        self.passed_time = 0
        self.timer_started = False
        self.start_time = 0
        self.controller = 1
        self.score_list = []
        self.increase_s = 20
        self.decrease_s = 40
        self.font_color = False

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

    def display_score(self):
        self.passed_time = pygame.time.get_ticks() - self.start_time
        score = str(int(self.passed_time // 100) / 10)
        label = font.render(f"Time:{score} sec", False, (250, 150, 180))
        label_2 = font.render(f"Apples:{self.eaten_apples} tk", False, (250, 150, 180))
        screen.blit(label, (20, 50))
        screen.blit(label_2, (270, 50))
        pg.display.update()
        clock.tick(60)
        return score

    def crash(self):
        if self.music_play:
            file = 'music/game_over.mp3'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(1)

        self.playing = False
        self.passed_time = pygame.time.get_ticks() - self.start_time
        self.paused = False
        self.g_over = True
        self.controller = 2

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

    def move_block(self):
        for block in self.BLOCK_list:
            for elem in block:
                if self.change:
                    elem.speedy = 9
                    elem.update()
                else:
                    elem.speedy = 5
                    elem.update()

    def draw_block(self, block_list):
        for block in block_list:
            for each in block:
                each.draw()

    def remove_block(self):
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

                            elem.respawn()
                            self.list_of_apples = self.list_of_apples[:-1]
                            self.eaten_apples -= 1
                            if self.eaten_apples < 0:
                                self.crash()
                        elif type(elem) == Block:
                            self.crash()
                            self.playing = False
                    if abs(elem.rect.right - snake.rect.left) < collision_tolerance:
                        snake.rect.left = elem.rect.right + 1

                    if abs(elem.rect.left - snake.rect.right) < collision_tolerance:
                        snake.rect.right = elem.rect.left - 1

                    if abs(elem.rect.right - snake.rect_body.left) < collision_tolerance:
                        snake.rect_body.left = elem.rect.right + 1
                    if abs(elem.rect.left - snake.rect_body.right) < collision_tolerance:
                        snake.rect_body.right = elem.rect.left - 1

    def game_loop(self):
        if self.playing and self.controller == 5:
            self.start_time = self.score_list[-1]
            self.score_list.append(self.start_time)
        if self.playing and self.controller == 2 or self.controller == 1:
            if self.music_play:
                file = 'music/musiccc.mp3'
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(-1)
            self.start_time = pygame.time.get_ticks()
            self.score_list.append(self.start_time)

        self.eaten_apples = 0
        self.list_of_apples = []
        snake = Snake()

        apple = Apple()
        bullet = Bullet()
        breakable_block = BreakableBlock()

        while self.playing:
            self.display_score()
            self.check_events()


            if self.START_KEY:
                self.playing = False

            # Movement
            snake.update()
            self.check_crash(snake)
            apple.update()
            breakable_block.update()
            bullet.update()
            # On screen
            if self.font_color is False:
                screen.fill("#ccffcc")
            elif self.font_color is True:
                screen.fill((0, 0, 0))

            screen.blit(snake.image, (snake.rect.x, snake.rect.y))
            screen.blit(apple.image, (apple.rect.x, apple.rect.y))

            # Blocks
            self.move_block()
            self.draw_block(self.BLOCK_list)
            self.remove_block()

            if (self.passed_time // 100 / 10) > self.increase_s:
                self.font_color = True
                self.change = True
                apple.speedy = 8
                snake.move = 7
                self.increase_s += 40

            elif (self.passed_time // 100 / 10) > self.decrease_s:
                self.font_color = False
                self.change = False
                apple.speedy = 6
                snake.move = 5
                self.decrease_s += 40

            if self.eaten_apples > -1:
                for x in self.list_of_apples:
                    new_variable = snake.rect_body.y + 26 * x
                    screen.blit(snake.image_body, (snake.rect_body.x, new_variable))

            if snake.rect.colliderect(apple.rect):
                self.eaten_apples += 1
                self.list_of_apples.append(self.eaten_apples)
                apple.respawn()

            key_state = pygame.key.get_pressed()
            if self.change:
                if key_state[pygame.K_SPACE]:
                    bullet.rect.y -= 100
                    if bullet.rect.y < -400:
                        bullet.rect.y = snake.rect.y + 10
                        bullet.rect.x = snake.rect.x
                    for smth in self.BLOCK_list:
                        for block in smth:
                            if type(block) == Block:
                                if bullet.rect.colliderect(block.rect):
                                    block.rect.x = random.randrange(west_b, east_b) + 1000
                                    bullet.rect.y = snake.rect.y + 10
                                    bullet.rect.x = snake.rect.x

                    screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

            if self.font_color is False:
                s = pygame.Surface((480, 720))
                s.set_alpha(0)  # alpha level
                s.fill((0, 0, 0))  # this fills the entire surface
                screen.blit(s, (0, 0))

            elif self.font_color is True:
                s = pygame.Surface((480, 720))
                s.set_alpha(90)  # alpha level
                s.fill((255, 0, 0))  # this fills the entire surface
                screen.blit(s, (0, 0))

            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.curr_menu.run_display = False
                self.curr_game_over.run_display = False
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.playing = False
                    self.paused = True
                    pygame.mixer.music.pause()
                    self.g_over = False
                    self.controller = 5

                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.EXIT_KEY = True
                    self.curr_menu.run_display = False
                    self.running, self.playing = False, False
                    quit()
                    pygame.quit()
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == SPAWNBLOCK and self.playing is True:
                self.BLOCK_list.append(self.create_block())

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


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

        self.move = 5

        self.speed_x = 10

    def update(self):

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= self.move
            self.rect_body.x -= self.move
        if key_state[pygame.K_RIGHT]:
            self.rect.x += self.move
            self.rect_body.x += self.move

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


snaky = Snake()


class Bullet:
    def __init__(self):
        self.image = bullet_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = int(w_width * 0.5)
        self.rect.y = int(w_height * 0.5) + 10

        self.speedy = 200

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= 5
        if key_state[pygame.K_RIGHT]:
            self.rect.x += 5

        # Check boundary
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.left > east_b:
            self.rect.left = east_b
