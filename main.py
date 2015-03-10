from blackjack import Blackjack
from blackjack_odds import BlackjackOddsSpecific
from blackjack_odds import BlackjackOddsAll


# Methods
def get_names_ui():
    name = input("Please enter your name (enter blank for default players): ")
    if not name:  # default
        players = ["junnu", "jenni"]
        print(" - Default selected, players: ", players, "\n")
    else:
        players = []
        while name and len(players) < 6:  # max players = 6
            players.append(name)
            name = input("Add more players (enter blank to finish): ")
    return players


def get_game_type():
    while True:
        game_type = input("Select game type: auto pilot / normal [default] / specific card / test all): ")
        if not game_type:  # default
            game_type = "normal"
            print(" - Default game type selected: ", game_type, "\n")
            break
        elif game_type == "normal" or game_type == "specific card" or game_type == "test all" or game_type == "auto pilot":
            break
        else:
            print(" - Unknown game type. Please use a proper game type.")
    return game_type


def get_rounds_count():
    rounds_count = input("Please specify, how many rounds do you want to play (default = 1000): ")
    if not rounds_count:  # default
        rounds_count = 1000
        print(" - Default rounds count selected: ", rounds_count, "\n")
    return rounds_count


# Main
print("Welcome to the game of Blackjack!")
game_type = get_game_type()

if game_type != "normal":
    while True:
        try:
            rounds_count = int(get_rounds_count())
            break
        except ValueError:
            print("please give a proper integer")

if game_type == "auto pilot":
    players = ["John", "Jenni"]
    game = Blackjack(players)
    game.start_game(rounds_count)

if game_type == "normal":
    players = get_names_ui()
    print("Manual game starts...\n")
    game = Blackjack(players, manual=True)
    game.start_game()

if game_type == "specific card":
    game = BlackjackOddsSpecific(players)
    game.start_game(rounds_count)

if game_type == "test all":
    # Creates a file with all possible hands with odds by action
    file_results = open("result.txt", "w")
    print("Player\t\t", "Dealer\t", "Stand\t", "Hit\t", "Double\t", "Split\t", file=file_results)

    game = BlackjackOddsAll(file_results)
    game.start_game(rounds_count)
    file_results.close()

