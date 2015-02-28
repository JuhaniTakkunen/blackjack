from blackjack import Blackjack
from player import Player
import time

# NOTE! THIS IS OUTDATED, modifications have been done to blackjack.py (counting cards) - 28.2.2015 - JT

class BlackjackOdds(Blackjack):
    def test_odds(self, number_of_rounds, player_card_values, dealer_card_value, fobj):
            actions = ["Stand", "Hit", "Double", "Split"]
            names = ["Jenni", "Teemu", "Junnu", "Matti"]
            self.players = [Player(name, action) for name, action in zip(names, actions)]
            for _ in range(0, number_of_rounds):
                self.start_odds_round(player_card_values, dealer_card_value)

            print(player_card_values, "\t", end="\t", file=fobj)
            print(dealer_card_value, end="\t", file=fobj)
            for player in self.players:
                print(player.get_money(), end="\t", file=fobj)
            print("", file=fobj)

    def start_odds_round(self, player_card_values, dealer_card_value):

        # Initialize players and (if needed) shuffle the deck.
        for player in self.players:
            player.new_round()
        self.dealer.new_round()
        self.deck.shuffled(self.number_of_decks)

        # Deal two SPECIFIC cards to each player and the dealer.
        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(player_card_values[0], hand)  # TODO: check that dealing is ok by odds
                self.deck.deal_value_card(player_card_values[1], hand)
        self.deck.deal_value_card(dealer_card_value, self.dealer.get_hand())
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds

        # Gameplay
        for player in self.players:
                self.player_turn(player, first_action=player.action)
        self.dealer_turn()

        # End game
        self.decide_winner()
