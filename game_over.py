import pygame

import menu
from menu import *



class GameOver():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H /2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class GameOverMain(GameOver):
    def __init__(self, game):
        GameOver.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionx, self.optiony = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_screen(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Game Over", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Continue", 20, self.startx, self.starty)
            self.game.draw_text("Exit", 20, self.optionx, self.optiony)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionx + self.offset, self.optiony)
                self.state = "Exit"
            # elif self.state == "Settings":
            #     self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            #     self.state = "Credits"
            # elif self.state == "Credits":
            #     self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            #     self.state = "Start"
        elif self.game.UP_KEY:
            # if self.state == "Start":
            #     self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            #     self.state = "Credits"
            if self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        if self.game.RUN_KEY:
            if self.state == "Start":
                self.game.game_over_screen = False
                self.game.playing = True
                self.game.BLOCK_list = []
                self.game.game_loop()
            elif self.state == "Exit":
                menu.MainMenu.display_menu(self.game.main_menu)
                self.game.playing = True


class OptionsMenu(GameOver):
    def __init__(self, game):
        GameOver.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.contrlosy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Exit", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.contrlosy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.contrlosy)
            elif self.state == "Controls":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.RUN_KEY:
            pass
