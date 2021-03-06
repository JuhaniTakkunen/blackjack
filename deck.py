# Deck defines the properties and functions, what deck can do
# - contains of 52 cards
# - cards can be dealt and shuffled
# - count cards based on Hi-Lo - strategy described in http://en.wikipedia.org/wiki/Card_counting#Systems
import itertools
from random import shuffle


class Card:
    def __init__(self, rank, suit):
        self.rank = str(rank)
        self.suit = suit

        if rank in ['K', 'Q', 'J']:
            self.value = 10
        elif rank in ["A"]:
            self.value = 1
        else:
            self.value = int(rank)

    def get_rank(self, show_royals=True):
        if not show_royals and self.value == 10:
            return str(10)
        else:
            return self.rank


class Deck:
    # contains n * 52 Cards
    def __init__(self):
        self.cards = []
        self.suits = ["spade", "hearts", "club", "diamond"]
        self.ranks = list(range(2, 11))
        self.ranks.extend(['A', 'K', 'Q', 'J'])
        self.name = "Deck"
        self.ratio_count = 0

    def cards_left(self):
        return len(self.cards)

    def shuffle_new(self, n):
        self.cards = []
        for _ in itertools.repeat(None, n):
            for rank, suit in list(itertools.product(self.ranks, self.suits)):
                self.cards.append(Card(rank, suit))
        shuffle(self.cards)  # Mersenne twister
        self.ratio_count = 0

    def shuffle_rest(self):
        shuffle(self.cards)  # Mersenne twister

    def show_cards(self):
        for card in self.cards:
            print(card.suit, card.rank)

    def deal(self, n, target):
        for card in self.cards[0:n]:
            # Update ratio for card counting
            if card.value == 1 or card.value == 10:
                self.ratio_count -= 1
            elif 6 >= card.value >= 2:
                self.ratio_count += 1

            target.add_card(card)
            self.cards.remove(card)

    def deal_value_card(self, rank, target, keep_in_deck=False):
        for card in self.cards:
            if card.get_rank() == rank:
                # Update ratio for card counting
                if card.value == 1 or card.value == 10:
                    self.ratio_count -= 1
                elif 6 >= card.value >= 2:
                    self.ratio_count += 1

                target.add_card(card)
                if not keep_in_deck:
                    self.cards.remove(card)
                return

        raise Exception("Card not found from deck")

    def get_ratio(self):
        return self.ratio_count / self.cards_left()*52
