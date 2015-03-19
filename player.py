from hand import Hand
import playbook


class Player():

    def __init__(self, name, first_action=None, counting=False):
        self.name = name
        self.money = 1000
        self.bet = 1
        self.hands = {}  # Hand(): Has hand ended (Stay / Over)
        self.default_first_action = first_action

        # counters
        self.round_count = 0
        self.win_count = 0
        self.tie_count = 0
        self.lose_count = 0
        self.blackjack_count = 0
        self.counting = counting
        self.rulebook = playbook.get_charts()

    def update_playbook(self):
        self.rulebook = playbook.get_charts()

    def new_round(self, deck=False):
        self.round_count += 1
        if self.counting:
            ratio = deck.get_ratio()
        else:
            ratio = 1
        if ratio:
            if ratio > 2:
                self.bet = int(ratio)
            else:
                self.bet = 1
        hand = Hand(self.bet)
        hand.default_first_action = self.default_first_action
        self.hands = {hand: False}

    def discard(self, hand):
        del self.hands[hand]

    def show_money(self):
        print(self.name, "has", self.money, "€ after", self.round_count, "rounds")

    def get_money(self):
        return self.money

    def win(self, hand, rules):
        self.win_count += 1
        if hand.is_blackjack():
            self.blackjack_count += 1
            hand.bet = hand.bet * rules.blackjack_win_ratio
            self.money += hand.bet
        else:
            self.money += hand.bet
        hand.status = "win"

    def lose(self, hand):
        self.lose_count += 1
        self.money -= hand.bet
        hand.status = "lose"

    def tie(self, hand):
        self.tie_count += 1
        hand.status = "tie"

    def set_money(self, money):
        self.money = money

    def split(self, hand):
        new_hand = hand.split()
        self.hands[new_hand] = False

    def number_of_hands(self):
        return len(self.hands)

    def has_next_hand(self):
        for hand in self.hands:
            if not self.hands[hand]:
                return True
        return False

    def next_hand(self):
        for hand in self.hands:
            if not self.hands[hand]:
                self.hands[hand] = True
                return hand
        raise Exception("No playable hands")

    def get_hands(self):
        return self.hands

    def move(self, hand, dealer_hand, use_chart=True):
        import action
        if use_chart:
            action = action.action_from_chart(self, hand, dealer_hand)
            return action
        else:
            action = action.action_monte_carlo(hand=hand, dealer_hand=dealer_hand, rounds=100)
            return action

