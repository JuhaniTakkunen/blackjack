import itertools
from random import shuffle


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        if rank in ['K', 'Q', 'J']:
            self.value = 10
        elif rank in ["A"]:
            self.value = 1
        else:
            self.value = int(rank)

    def get_rank(self, show_royals=True):
        if not show_royals and self.value == 10:
            return 10
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
        self.ratio = 0

    def cards_left(self):
        return len(self.cards)

    def shuffled(self, n):
        self.cards = []
        for _ in itertools.repeat(None, n):
            for card in list(itertools.product(self.ranks, self.suits)):
                self.cards.append(Card(card[0], card[1]))
        shuffle(self.cards)
        self.ratio = 0

    def show_cards(self):
        for card in self.cards:
            print(card.suit, card.rank)

    def deal(self, n, target):
        for card in self.cards[0:n]:
            if card.value == 1 or card.value == 10:
                self.ratio -= 1
            elif 6 >= card.value >= 2:
                self.ratio += 1
            target.add_card(card)
            self.cards.remove(card)

    def deal_value_card(self, rank, target):
        for card in self.cards:
            if card.get_rank() == rank:
                target.add_card(card)
                self.cards.remove(card)
                return
        raise Exception("Card not found from deck")