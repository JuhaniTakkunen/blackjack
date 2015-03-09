from blackjack import Blackjack
import time


class BlackjackOdds(Blackjack):

    def deal_initial(self):
        self.deck.shuffle_all(self.number_of_decks)  # every round is a "new" round
        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(self.player_card_1_value, hand)  # TODO: check that dealing is ok by odds
                self.deck.deal_value_card(self.player_card_2_value, hand)
        self.deck.deal_value_card(self.dealer_card_value, self.dealer.get_hand())
        self.deck.shuffle_rest()  # not sure if needed
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds


class BlackjackOddsSpecific(BlackjackOdds):

    def __init__(self, player, dealer):
        Blackjack.__init__(self, player, dealer)
        self.player_card_1_value = input("Select player card 1 (A, 2-10, J, Q, K): ")
        self.player_card_2_value = input("Select player card 2 (A, 2-10, J, Q, K): ")
        self.dealer_card_value = input("Select dealer card 1 (A, 2-10, J, Q, K): ")


class BlackjackOddsAll(Blackjack):

    def __init__(self, file_object):
        Blackjack.__init__(self, ["Hit", "Stand", "Split", "Double"], "Dealer")
        self.file_object = file_object
        self.player_card_1_value = ""
        self.player_card_2_value = ""
        self.dealer_card_value = ""

    def start_game(self, number_of_rounds):
        all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
        for self.player_card_1_value in all_cards:
            for self.player_card_2_value in all_cards:
                for self.dealer_card_value in all_cards:
                    # TODO!! Initialize deck and players (money + counting)
                    for _ in range(0, number_of_rounds):
                        self.start_round()
                    print(self.player_card_1_value, "done at", time.strftime("%H:%M:%S"))
                    self.print_results_to_file()

    def print_results_to_file(self):
        print(self.player_card_1_value, self.player_card_2_value, "\t", end="\t", file=self.file_object)
        print(self.dealer_card_value, end="\t", file=self.file_object)
        for player in self.players:
            print(player.get_money(), end="\t", file=self.file_object)
        print("", file=self.file_object)

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

