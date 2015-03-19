def action_from_chart(player, hand, dealer_hand):
    dealer_ranks = dealer_hand.get_card_ranks(n_cards=1, show_royal=False)
    player_ranks = hand.get_card_ranks(show_royal=False)
    if hand.can_split() is True:  # two cards with the same value
        search_word = str(player_ranks[0]) + ' ' + str(player_ranks[1])  # TODO: invent better variable name (search_word)
        action = player.rulebook[search_word][str(dealer_ranks[0])]  # csv-file format | TODO: rename rulebook -> playbook
    elif hand.has_ace() and hand.can_double():  # "soft" double has different odds than "hard"
        if player_ranks[0] is "A":
            search_word = str(player_ranks[0]) + ' ' + str(player_ranks[1])
        else:
            search_word = str(player_ranks[1]) + ' ' + str(player_ranks[0])
        action = player.rulebook[search_word][str(dealer_ranks[0])]
    else:
        points = hand.sum_of_cards(as_text=True)

        try:
            action = player.rulebook[(points, str(dealer_ranks[0]))]
        except TypeError:
            print("FAIL in action.py.action_from_chart().player.rulebook")
            print(points, str(dealer_ranks[0]))
            print("-------")
            print(player.rulebook)
        except KeyError:
            print("FAIL in action.py.action_from_chart().player.rulebook")
            print(points, str(dealer_ranks[0]))
            print("-------")
            print(player.rulebook)

    if action == "Double" and not hand.can_double():
        raise Exception("illegal double")
    elif action == "Split" and not hand.can_split():
        raise Exception("illegal split")
    return action


def action_monte_carlo(hand, dealer_hand, rounds):
    import blackjack_odds
    monte_carlo = blackjack_odds.BlackjackOddsSpecificAuto(hand, dealer_hand)
    monte_carlo.start_game(rounds)

    max_money = float("-inf")
    for player in monte_carlo.players:
        if player.money > max_money:
            max_money = player.money
            max_name = player.name

    return max_name