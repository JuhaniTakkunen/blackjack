from hand import Hand


class Dealer():
    def __init__(self):
        self.hand = None

    def new_round(self):
        self.hand = Hand(0)

    def move(self, rules):
        if self.hand.sum_of_cards() <= rules.dealer_hit_value_max:
            return "Hit"
        else:
            return "Stand"

    def get_hand(self):
        return self.hand