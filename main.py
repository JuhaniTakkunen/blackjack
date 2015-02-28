from blackjack import Blackjack
from blackjack_gui import start_gui
from tkinter import *



# Initialize graphics
root = Tk()
gui = start_gui(root)

# Set up game - user input
players = gui.get_players()
print(players)
dealer = gui.get_dealer()
print(dealer)

# Start game
game = Blackjack(players, dealer, gui=False)
game.start_game(1000)


