
def ui_continue_game(game):
    while True:
        var = input("Do you want to continue? [y/n/change bet] (default=y): ")
        if not var:
            var = "y"
        if var == "y" or var == "Y":
            return True
        elif var == "n" or var == "N":
            return False
        if var == "change bet":
            for player in game.players:
                while True:
                    try:
                        var = int(input("Set bet for "+player.name+": "))
                        if var <= 0:
                            raise ValueError("not a positive number!")
                        break
                    except ValueError:
                        print("ValueError, use a positive integer")
                player.bet = var
        else:
            print("Please answer 'y', 'n' or 'change bet'")


def ui_player_action(player, hand, game, default):
    while True:
        print("Player", player.name, hand.sum_of_cards(), "points: ")
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