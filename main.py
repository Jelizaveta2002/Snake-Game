from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    if g.start:
        g.game_loop()
