from blackjack import Blackjack
from player import Player

class BlackjackOdds(Blackjack):

    def deal_initial(self):

        player_card_values = [2,2]
        dealer_card_value = "A"

        self.deck.shuffle_all(self.number_of_decks)  # every round is a "new" round
        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(player_card_values[0], hand)  # TODO: check that dealing is ok by odds
                self.deck.deal_value_card(player_card_values[1], hand)
        self.deck.deal_value_card(dealer_card_value, self.dealer.get_hand())
        self.deck.shuffle_rest()  # not sure if needed
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds



    # # OUTDATED STUFF
    #
    # def test_odds(self, number_of_rounds, player_card_values, dealer_card_value, *fobj):
    #     actions = ["Stand", "Hit", "Double", "Split"]
    #     names = ["Jenni", "Teemu", "Junnu", "Matti"]
    #     self.players = [Player(name, action) for name, action in zip(names, actions)]
    #     for _ in range(0, number_of_rounds):
    #         self.start_odds_round(player_card_values, dealer_card_value)
    #
    #     if fobj:
    #         print(player_card_values, "\t", end="\t", file=fobj)
    #         print(dealer_card_value, end="\t", file=fobj)
    #         for player in self.players:
    #             print(player.get_money(), end="\t", file=fobj)
    #         print("", file=fobj)
    #
    #     self.dealer.get_hand().show_cards()
    #     money = 0
    #     # Print results
    #     print("---")
    #     for player in self.players:
    #         player.show_money()
    #         # TODO: GUI - show money
    #         money += player.get_money()
    #         print("odds are for the house: ", (1000 - money/len(self.players))/number_of_rounds*100, "percent")
    #         print("wins", player.win_count, "lost", player.lose_count, "tie", player.tie_count)
    #
    # def start_odds_round(self, player_card_values, dealer_card_value, counting=False):
    #
    #     # Initialize players and (if needed) shuffle the deck.
    #     for player in self.players:
    #         if counting:
    #             ratio = self.deck.ratio / self.deck.cards_left()*52
    #         else:
    #             ratio = 0
    #         player.new_round(ratio)
    #     self.dealer.new_round()
    #     self.deck.shuffle_all(self.number_of_decks)
    #
    #     # Deal two SPECIFIC cards to each player and the dealer.
    #     for player in self.players:
    #         for hand in player.get_hands():
    #             self.deck.deal_value_card(player_card_values[0], hand)  # TODO: check that dealing is ok by odds
    #             self.deck.deal_value_card(player_card_values[1], hand)
    #     self.deck.deal_value_card(dealer_card_value, self.dealer.get_hand())
    #     self.deck.shuffle_rest()  # not sure if needed
    #     self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds
    #
    #     # Gameplay
    #     for player in self.players:
    #             self.player_turn(player, first_action=player.action)
    #     self.dealer_turn()
    #
    #     # End game
    #     self.decide_winner()
