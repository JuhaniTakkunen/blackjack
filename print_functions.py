# Here is a list of functions which can be used to print information to console. Functions are mostly taken from
# blackjack.py to make the code in that file easier to read. There are still print commands in other files!
# Known files to have printing properties:
# - blackjack_ui.py
# - blackjack_odds.py


# main.py
def print_welcome():
    print("Welcome to the game of Blackjack!")


def print_start_manual():
    print("Manual game starts...\n")


# blackjack.py
def print_results(players, rounds):
    print("")
    print("--- *** RESULTS *** ---")
    print("")
    total_win_count, total_lose_count, total_tie_count, total_money_count = 0, 0, 0, 0

    for player in players:
        player.show_money()
        odds = (1000 - player.get_money())/rounds*100
        print("odds are for the house: ", odds, "percent")
        print("wins", player.win_count, "lost", player.lose_count, "tie", player.tie_count)
        print("")
        total_win_count += player.win_count
        total_lose_count += player.lose_count
        total_tie_count += player.tie_count
        total_money_count += player.get_money()

    print("--- combined results ---")
    odds = (1000*len(players) - total_money_count)/(rounds*len(players))*100
    print("odds are for the house: ", odds, "percent")
    print("wins", total_win_count, "lost", total_lose_count, "tie", total_tie_count)
    print("")


def print_busted(player, hand):
    print(" ---- Player", player.name, "busted with", hand.sum_of_cards(), "points. ---- ")


def print_double(player, hand):
    print("Player", player.name, "stays after double with: ", hand.sum_of_cards(), "points, ", end="")
    hand.show_cards()
    print("\n")


def print_round_ended(game):
    print("Round", game.round_count, "ended")
    print("Dealer hand", game.dealer.hand.sum_of_cards(), "points: ", end="")
    game.dealer.hand.show_cards()


def print_player_round_stats(blackjack):
    for player in blackjack.players:
        for hand in player.get_hands():
            print("Player", player.name, hand.status, hand.bet, "€ with", hand.sum_of_cards(), "points: ", end="")
            hand.show_cards()
    print("\n \t Total money ")
    for player in blackjack.players:
        print("\t", player.name, player.money, "€")
    print(" ")


def print_player_turn(player):
    print("\n ---- Player", player.name, "turn! ---- \n")


def print_default_chart(file_name):
    print("Copying default cheat charts from: ", file_name)