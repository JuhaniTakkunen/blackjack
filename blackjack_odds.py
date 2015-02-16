from blackjack import Blackjack
from player import Player
import time


class BlackjackOdds(Blackjack):
    def test_odds(self, number_of_rounds, player_card_values, dealer_card_value, fobj):
            actions = ["Stand", "Hit", "Double", "Split"]
            players = ["Jenni", "Teemu", "Junnu", "Matti"]
            self.players = [Player(name, action) for name, action in zip(players, actions)]
            for _ in range(0, number_of_rounds):
                self.start_odds_round(player_card_values, dealer_card_value)

            print(player_card_values,"\t", end="\t", file=fobj)
            print(dealer_card_value, end="\t", file=fobj)
            for player in self.players:
                print(player.get_money(), end="\t", file=fobj)
            print("", file=fobj)

    def start_odds_round(self, player_card_values, dealer_card_value):

        for player in self.players:
            player.new_round()
        self.dealer.new_round()

        self.deck.shuffled(self.number_of_decks)
        # Deal two cards to each player and dealer

        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(player_card_values[0], hand)
                self.deck.deal_value_card(player_card_values[1], hand)

        self.deck.deal_value_card(dealer_card_value, self.dealer.get_hand())
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds

        # Gameplay
        for player in self.players:
                self.player_turn(player, first_action=player.action)

        self.dealer_turn()
        # End game
        self.decide_winner()

#def Main():
players = ["Jenni", "Teemu", "Junnu", "Matti"]
dealer = "Teemu"
file_results = open("result.txt", "w")
print("Player\t\t", "Dealer\t", "Stand\t", "Hit\t", "Double\t", "Split\t", file=file_results)
game = BlackjackOdds(players, dealer)
all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
for i in all_cards:
    for j in all_cards:
        for k in all_cards:
            game.test_odds(1000, [k, j], i, file_results)
    print(i, "done at", time.strftime("%H:%M:%S"))

file_results.close()