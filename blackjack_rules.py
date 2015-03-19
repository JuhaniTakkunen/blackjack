

class BlackjackRules():
    # Class BlackjackRules defines the rules of blackjack. Blackjack rules have multiple variations, and here we use the
    # following rules:
    # - dealer hits on 16 stands on 17
    # - money returns to player in case of tie
    # - blackjack pays 3:2
    # - hand can be split only once after first two cards are dealt and they have the same value
    # - double is not allowed for split hands
    # - double can be done, if first two cards have a value in range of 9-11 # TODO: check this
    # - player if allowed, if he/she so chooses, hit on 21
    def __init__(self):
        self.number_of_decks = 6  # Typical number of decks in casinos
        self.cards_left_min = 30
        self.dealer_hit_value_max = 16  # Hit on 16, stand on 17
        self.blackjack_win_ratio = 1.5

    def decide_winner(self, blackjack):
        # blackjack is an object of the class Blackjack()
        # http://www.wikihow.com/Sample/Blackjack-Rules
        dealer_hand = blackjack.dealer.hand
        for player in blackjack.players:
            for hand in player.get_hands():
                if hand.sum_of_cards() > 21:
                    player.lose(hand)
                elif dealer_hand.sum_of_cards() > 21:
                    player.win(hand, self)
                elif hand.is_blackjack() and not dealer_hand.is_blackjack():  # Player blackjack wins
                    player.win(hand, self)
                elif dealer_hand.is_blackjack() and not hand.is_blackjack():  # House blackjack wins
                    player.lose(hand)
                elif hand.sum_of_cards() == dealer_hand.sum_of_cards():  # Tie, important that we check blackjacks first
                    player.tie(hand)
                elif hand.sum_of_cards() > dealer_hand.sum_of_cards():
                    player.win(hand, self)
                elif hand.sum_of_cards() < dealer_hand.sum_of_cards():
                    player.lose(hand)
                else:
                    # One never is here, I hope
                    print("ERROR - unable to determine winner")
                    print("Player", player.name, "cards: ")

    def is_action_allowed(self, action, hand):
        if action == "Double":
            return hand.can_double()
        if action == "Split":
            return hand.can_split()
        if action == "Hit":
            if hand.sum_of_cards() >= 21:
                return False
            if hand.is_blackjack():
                return False  # Player has to win :P
            else:
                return True
        if action == "Stand" or action == "Stay":
            return True
        else:
            print(action)
            raise RuntimeError("No corresponding action found in is_action_allowed")
