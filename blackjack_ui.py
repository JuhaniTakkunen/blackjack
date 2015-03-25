# This file contains user interface functions for blackjack game. Functions are in separate file to make code in other
# files easier to read, but also this way translations and graphical UI can be added later more easily.
# - Juhani Takkunen, juhani.takkunen@gmail.com


# functions originally copied from blackjack.py
def ui_set_bet(players):
    for player in players:
                while True:
                    try:
                        var = int(input("Set bet for "+player.name+": "))
                        if var <= 0:
                            raise ValueError("not a positive number!")
                        break
                    except ValueError:
                        print("ValueError, use a positive integer")
                player.bet = var


def ui_continue_game(game):
    import print_functions
    print_functions.print_round_ended(game)
    print_functions.print_player_round_stats(game)
    while True:
        var = input("Do you want to continue? [y/n/change bet] (default=y): ")
        if not var:
            var = "y"
        if var == "y" or var == "Y":
            return True
        elif var == "n" or var == "N":
            return False
        if var == "change bet":
            ui_set_bet(game.players)
        else:
            print("Please answer 'y', 'n' or 'change bet'")


def ui_player_action(player, hand, game, default):
    while True:
        print("Player", player.name, hand.sum_of_cards(as_text=True))
        hand.show_cards()
        print("Dealer cards: ")
        game.dealer.hand.show_cards(1)
        text = "Choose action [hit, stay"
        if hand.can_double():
            text += ", double"
        if hand.can_split():
            text += ", split"
        var = input(text+"], (default = "+default+"): ")
        if not var:
            var = default
            print(" - default action: ", default, "\n")
        if var == "Split" or var == "split":
            if hand.can_split():
                action = "Split"
            else:
                print(" - sorry, split not allowed, choose another action.")
        elif var == "Stay" or var == "stay" or var == "Stand" or var == "stand":
            action = "Stay"
        elif var == "Hit" or var == "hit":
            action = "Hit"
        elif var == "Double" or var == "double":
            if hand.can_double():
                action = "Double"
            else:
                print(" - sorry, split not allowed, choose another action.")
        else:
            print("- Invalid action, allowed actions are: split, stay, hit or double.")
            continue
        break
    return action


# functions originally copied from main.py
def ui_get_names():
    name = input("Please enter your name (enter blank for default players): ")
    if not name:  # default
        name_list = ["junnu", "jenni"]
        print(" - Default selected, players: ", name_list, "\n")
    else:
        name_list = []
        while name and len(name_list) < 6:  # max players = 6
            name_list.append(name)
            name = input("Add more players (enter blank to finish): ")
    return name_list


def ui_get_game_type():
    while True:
        user_input = input("Select game type: auto pilot / normal [default] / specific card / create charts): ")
        if not user_input:  # default
            user_input = "normal"
            print(" - Default game type selected: ", user_input, "\n")
            break
        elif user_input in ["normal", "specific card", "create charts", "auto pilot"]:
            break
        else:
            print(" - Unknown game type. Please use a proper game type.")
    return user_input


def ui_get_rounds_count():
    while True:
        try:
            user_input = input("Please specify, how many rounds do you want to play (default = 1000): ")
            if not user_input:  # default
                user_input = 1000
                print(" - Default rounds count selected: ", user_input, "\n")
            else:
                user_input = int(user_input)
            if user_input <= 0:
                raise ValueError("Positive value required.")
            elif user_input > 100000:
                confirm = input("You have selected a high rounds count - please confirm "+str(user_input)+" [y/n] : ")
                if confirm in ["y", "Y", "yes", "YES", "Hell yeah!"]:
                    pass
                else:
                    print("Confirmation failed.")
                    raise ValueError
            return user_input
        except ValueError:
            print(" - ValueError: positive integer not found.")


def ui_get_counting(player):
    user_input = input("Do you "+player.name+" want to count cards? [y/n]: ")
    if user_input in ["y", "Y"]:
        player.counting = True
    elif not user_input:
        print("- Default setting - no counting")