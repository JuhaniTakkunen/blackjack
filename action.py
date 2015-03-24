def action_from_chart(player, hand, dealer_hand):
    dealer_ranks = dealer_hand.get_card_ranks(n_cards=1, show_royal=False)
    points = hand.sum_of_cards(as_text=True)
    rules = player.rulebook[(points, str(dealer_ranks[0]))]
    for action in rules:
        # Skip illegal actions
        if action == "Double" and not hand.can_double():
            continue
        elif action == "Split" and not hand.can_split():
            continue
        else:
            return action


def action_monte_carlo(hand, dealer_hand, rounds):  # TODO: Check this
    import blackjack_odds
    monte_carlo = blackjack_odds.BlackjackOddsSpecificAuto(hand, dealer_hand)
    monte_carlo.start_game(rounds)

    max_money = float("-inf")
    for player in monte_carlo.players:
        if player.money > max_money:
            max_money = player.money
            max_name = player.name
    return max_name