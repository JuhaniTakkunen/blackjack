from blackjack import Blackjack
from blackjack_odds import *  # TODO: check what imports we truly need
from blackjack_ui import *  # all functions with prefix ui_ are in this file
from print_functions import *  # all functions with prefix print_ are in this file

# Main
print_welcome()
game_type = ui_get_game_type()

if game_type != "normal":
    rounds_count = ui_get_rounds_count()

if game_type == "auto pilot":
    name_list = ["John", "Jenni"]
    game = Blackjack(name_list)
    for player in game.players:
        ui_get_counting(player)
    game.start_game(rounds_count)

if game_type == "normal":
    name_list = ui_get_names()
    print_start_manual()
    game = Blackjack(name_list, manual=True)
    game.start_game()

if game_type == "specific card":
    name_list = ui_get_names()
    game = BlackjackOddsSpecificManual(name_list)
    game.start_game(rounds_count)

if game_type == "create charts":
    # Creates a file with all possible hands with odds by action

    # File names (tmp. -files are removed in the end)
    file1_name = 'blackjack_chart.csv'
    file2_name = 'tmp.blackjack_chart_double_split.csv'

    # Create headers
    with open(file1_name, "w") as file_object:
        print("Player,\t\t", "Dealer,\t", "Hit,\t", "Stand", file=file_object)
    with open(file2_name, "w") as file_object:
        print("Player,\t\t", "Dealer,\t", "Double,\t", "Split", file=file_object)

    # Run simulations
    game = BlackjackOddsStandHit(file1_name)
    game.start_game(rounds_count)
    game2 = BlackjackOddsDoubleSplit(file2_name)
    game2.start_game(rounds_count)

    # Print results to a single file
    import playbook
    rulebook_1 = playbook.get_charts(file1_name, return_odds=True)
    rulebook_2 = playbook.get_charts(file2_name, return_odds=True)
    rulebook_final = {}
    for cards, actions in rulebook_1.items():
        rulebook_final[cards] = actions+rulebook_2[cards]

    with open("tmp."+file1_name, "w") as file_object:
        actions = ["Hit", "Stand", "Double", "Split"]
        # HEADER
        print("Player,\t\t", "Dealer,\t", ",\t".join(x for x in actions), file=file_object)

        # VALUES
        for cards, values in sorted(rulebook_final.items()):
            print(', \t'.join(cards), ",\t", ",\t".join(format(x, ".3f") for x in values), file=file_object)

    # Update the chart file and remove unnecessary files (tmp. -prefix)
    import shutil
    import os
    shutil.copyfile(src="tmp."+file1_name, dst=file1_name)
    os.remove("tmp."+file1_name)
    os.remove(file2_name)