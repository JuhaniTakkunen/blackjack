def get_charts(book_id="default"):
        if book_id == "wiki":
            # Load rulebook on how to play each the BlackJack in each scenario
            import csv
            with open('Blackjack-chart.csv', 'rt', encoding="UTF-8") as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                dealer_card = next(data, None)
                rulebook = {}
                for row in data:
                    hand_action = {}
                    for i in range(1, len(dealer_card)):
                        hand_action[dealer_card[i]] = row[i]
                    rulebook[row[0]] = hand_action
        elif book_id == "default":
            # Load rulebook on how to play each the BlackJack in each scenario
            import csv
            import operator

            rulebook = {}
            for file_name in ['blackjack_chart_hit_stand.csv', 'blackjack_chart_double_split.csv']:
                with open(file_name, 'rt', encoding="UTF-8") as csv_file:
                    data = csv.reader(csv_file, skipinitialspace=True, delimiter=',')
                    action = next(data, None)
                    action = action[2:]
                    for row in data:
                        player_hand_value = row[0]
                        dealer_card_value = row[1]
                        expected_return = row[2:]
                        odds = dict(zip(action, expected_return))
                        best_action = max(odds.items(), key=operator.itemgetter(1))[0]
                        rulebook[(player_hand_value.strip(), dealer_card_value.strip())] = best_action.strip()
        return rulebook