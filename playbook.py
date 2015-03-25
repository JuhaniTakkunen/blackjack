# Playbook loads "cheat" charts from given file.
# - if no file is given, default file is used
# - if no default file is found, default file is loaded from backup file
# Reason why these two actions are separated is that a new default file is always created when using "create charts"


def get_charts(file_id="blackjack_chart.csv", return_odds=False):
    # LOAD ODDS FROM FILE
    import csv
    import operator
    import os.path
    import shutil
    import print_functions
    import math

    if not os.path.isfile(file_id):
        # No file found, load backup default file
        print_functions.print_default_chart("blackjack_chart_default.csv")
        shutil.copyfile(src="blackjack_chart_default.csv", dst=file_id)
    file_name = file_id
    with open(file_name, 'rt', encoding="UTF-8") as csv_file:
        data = csv.reader(csv_file, skipinitialspace=True, delimiter=',')
        action_name = next(data, None)  # header (action) names
        action_name = action_name[2:]  # ignore first two names "Player" and "Dealer"

        # CREATE CHART FROM DATA
        # - remove duplicates
        # - order by best odds
        rulebook_odds = {}
        for row in data:
            player_hand_value = row[0].strip()
            dealer_card_value = row[1].strip()
            expected_return = row[2:]
            odds = dict(zip(action_name, expected_return))

            for action, value in odds.items():
                action = action.strip()
                value = value.strip()
                try:
                    value = float(value)
                except ValueError:
                    value = float("NaN")

                # Remove duplicates - pick the best odds value
                key = (player_hand_value, dealer_card_value)
                if key in rulebook_odds:
                    if action in rulebook_odds[key]:
                        if rulebook_odds[key][action] < value or math.isnan(rulebook_odds[key][action]):
                            rulebook_odds[key][action] = value
                        else:
                            continue  # new value is worse than the old value -> ignore it
                    else:
                        rulebook_odds[key][action] = value
                else:
                    rulebook_odds[key] = {action: value}

    # order actions by odds value
    rulebook = {}
    for cards, odds in rulebook_odds.items():
        if return_odds:
            ordered_odds = []  # ordered alphabetically by actions
            for action, odd in sorted(odds.items(), reverse=False, key=operator.itemgetter(0)):
                ordered_odds.append(odd)
            rulebook[cards] = ordered_odds
        else:
            ordered_actions = []
            for action, odd in sorted(odds.items(), reverse=True, key=operator.itemgetter(1)):
                if not math.isnan(odd):
                    ordered_actions.append(action.strip())
            rulebook[cards] = ordered_actions
    return rulebook