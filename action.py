# Functions return best action for given hand - either from file or by calculating it using Monte Carlo method.
def action_from_chart(player, hand, dealer_rank):
    points = hand.sum_of_cards(as_text=True)
    rules = player.rulebook[(points, dealer_rank)]
    for action in rules:
        # Skip illegal actions
        if action == "Double" and not hand.can_double():
            continue
        elif action == "Split" and not hand.can_split():
            continue
        else:
            return action


def action_monte_carlo(hand, dealer_rank, rounds):  # TODO: Check this
    import blackjack_odds
    monte_carlo = blackjack_odds.BlackjackOddsSpecificAuto(hand, dealer_rank)
    monte_carlo.start_game(rounds)

    max_money = float("-inf")
    for player in monte_carlo.players:
        if player.money > max_money:
            max_money = player.money
            max_name = player.name
    return max_name