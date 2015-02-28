from blackjack import Blackjack
from blackjack_gui import start_gui
from tkinter import *

use_gui = False
test_odds = False

if use_gui:
    # Initialize graphics
    root = Tk()
    gui = start_gui(root)

    # Set up game - user input
    players = gui.get_players()
    print(players)
    dealer = gui.get_dealer()
    print(dealer)
else:
    players = ["veikko", "jenni", "junnu", "apina", "vaeea"]
    dealer = "teemu"

if test_odds == False:
    # Start game
    players = ["veikko", "Jenni"]
    game = Blackjack(players, dealer, gui=False, debugging=True, pcv=[8,3], dcv=3)
    game.start_game(1)


if test_odds == True:
    from blackjack_odds import BlackjackOdds
    # def Main():
    # Creates a file with all possible hands with odds by action
    file_results = open("result.txt", "w")
    print("Player\t\t", "Dealer\t", "Stand\t", "Hit\t", "Double\t", "Split\t", file=file_results)
    game = BlackjackOdds(players, dealer)
    all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
    for i in all_cards:
        for j in all_cards:
            for k in all_cards:
                game.test_odds(1000, [k, j], i, file_results)
        print(i, "done at", time.strftime("%H:%M:%S"))

    file_results.close()

