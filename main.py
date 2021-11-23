from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    g.curr_game_over.display_screen()
