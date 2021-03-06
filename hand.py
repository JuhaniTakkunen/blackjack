# In Blackjack dealer and players have a hand of cards - players can even have multiple hands.
# Hands have at least the following properties:
# - cards
# - bet
# - hand status (pending / ended)
# - has hand been split (not always allowed to split multiple times)
#
# Bets are defined by hand, since a player can have multiple hands.


class Hand():
    def __init__(self, bet):  # TODO: bet=None would be better, but needs to be tested before implementing
        self.cards = []
        self.bet = bet
        self.has_split = False
        self.status = None
        self.default_first_action = None

    def has_ace(self):
        for card in self.cards:
            if card.get_rank() is "A":
                return True
        return False

    def has_splitted(self):  # sic(typo)!
        if self.has_split:
            return True
        else:
            return False

    def can_split(self):
        if len(self.cards) == 2 and not self.has_split:
            if self.cards[0].value == self.cards[1].value:
                return True
        else:
            return False

    def split(self):
        if self.can_split():
            new_hand = Hand(self.bet)
            new_hand.add_card(self.cards[1])
            self.remove_card(self.cards[1])
            self.has_split = True
            new_hand.has_split = True
            return new_hand
        else:
            raise Exception("Hand not splittable")

    def doublebet(self):
        self.bet = self.bet*2
        return self.bet

    def is_blackjack(self):
        if (
                len(self.cards) == 2 and (
                    (self.cards[0].value == 10 and self.cards[1].value == 1) or
                    (self.cards[0].value == 1 and self.cards[1].value == 10)
                )
        ):
            return True
        else:
            return False

    def show_cards(self, n=''):
        if n == 1:
            print(self.cards[0].suit, self.cards[0].rank)
        elif not n:
            for card in self.cards:
                print(card.suit, card.rank, end=", ")
        else:
            print("invalid n for show_cards")
        print("")

    def sum_of_cards(self, as_text=False):
        points = 0
        ace_count = 0
        for card in self.cards:
            if card.rank in ["J", "Q", "K"]:
                points += 10
            elif card.rank in ["A"]:
                points += 11
                ace_count += 1
                if points > 21:
                    points -= 10
                    ace_count -= 1
            else:
                points += int(card.rank)

            if points > 21 and ace_count > 0:
                points -= 10
                ace_count -= 1
        if as_text:
            if ace_count > 0:
                prefix = "Soft"
            else:
                prefix = "Hard"
            return prefix + " " + str(points)
        else:
            return points

    def discard_all(self):
        self.cards = []

    def get_cards(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def replace_cards(self, card1, card2):
        # FOR DEBUGGING ONLY!
        # replaces entire hand with given cards
        self.cards = [card1, card2]

    def remove_card(self, card):
        self.cards.remove(card)

    def get_card_ranks(self, n_cards=None, show_royal=True):
        result = []
        for card in self.cards:
            str(result.append(card.get_rank(show_royals=show_royal)))
        if n_cards is None:
            return result
        if n_cards == 1:
            return result[0]
        else:
            return result[0:n_cards]

    def can_double(self):
        if not self.has_splitted() and len(self.cards) == 2 and (9 <= self.sum_of_cards() <= 11):
            return True
        else:
            return False