# BlackjackOdds (and its subclasses) extend/replace Blackjack() class. Can be used to deal specific cards, multiple
# times. Name "BlackjackOdds" comes from this property - odds can be calculated using Monte Carlo - method.
from blackjack import Blackjack
import time


class BlackjackOdds(Blackjack):
    def __init__(self, players, file_name=None):
        Blackjack.__init__(self, players)
        for player in self.players:
            player.default_first_action = player.name
        self.file_name = file_name
        self.player_card_1_value = ""
        self.player_card_2_value = ""
        self.dealer_card_value = ""
        self.start_money = 1000
        self.rules.number_of_decks = 8
        self.keep_in_deck = True

    def calculate_odds(self, all_cards, number_of_rounds):
        # TODO: Parallelization can save computation time
        #       - parallelization should probably be done at higher level to minimize operations
        #       - one must be very careful not to let different threads to touch player.object variables)
        for self.dealer_card_value in all_cards:
            for player in self.players:
                player.set_money(self.start_money)
                player.update_playbook()
            for _ in range(0, number_of_rounds):
                self.start_round()
            self.print_results_to_file(number_of_rounds)

    def print_results_to_file(self, number_of_rounds):
        # TODO: This function works, but can be easily simplified
        if self.player_card_1_value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            prefix = "Hard"
            sum_of_cards = int(self.player_card_1_value)
        elif self.player_card_1_value == "A":
            prefix = "Soft"
            sum_of_cards = 11
        else:
            raise Exception("Unsupported card found")

        if self.player_card_2_value == "A":
            sum_of_cards += 11
            prefix = "Soft"
            if sum_of_cards == 22:
                sum_of_cards = 12
                if self.player_card_1_value != "A":
                    prefix = "Hard"
        else:
            sum_of_cards += int(self.player_card_2_value)

        with open(self.file_name, "a") as file_object:
            print(prefix, sum_of_cards, end=", \t \t", file=file_object)
            print(self.dealer_card_value, end=",  \t", file=file_object)
            for player in self.players:
                try:
                    money = str("{:3.4f}".format((player.get_money()-self.start_money)/number_of_rounds))
                except TypeError:
                    money = " None "
                print(money, end=", \t", file=file_object)
            print("", file=file_object)

    def deal_initial(self):
        self.deck.shuffle_new(self.rules.number_of_decks)  # every round is a "new" round
        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(self.player_card_1_value, hand, self.keep_in_deck)
                self.deck.deal_value_card(self.player_card_2_value, hand, self.keep_in_deck)
        self.deck.deal_value_card(self.dealer_card_value, self.dealer.get_hand())
        self.deck.shuffle_rest()
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds


class BlackjackOddsSpecificAuto(BlackjackOdds):

    def __init__(self, hand, dealer_rank):
        self.keep_in_deck = True
        players = ["Stand", "Hit", "Double", "Split"]
        Blackjack.__init__(self, players)
        self.hand = hand
        self.dealer_rank = dealer_rank

    def deal_initial(self):
        value = []
        for card in self.hand.cards:
                    value.append(card.rank)
        self.player_card_1_value = value[0]
        self.player_card_2_value = value[1]
        self.dealer_card_value = self.dealer_rank
        BlackjackOdds.deal_initial(self)


class BlackjackOddsSpecificManual(BlackjackOdds):

    def __init__(self, player):
        self.keep_in_deck = False
        Blackjack.__init__(self, player)
        self.player_card_1_value = input("Select player card 1 (A, 2-10, J, Q, K): ")
        self.player_card_2_value = input("Select player card 2 (A, 2-10, J, Q, K): ")
        self.dealer_card_value = input("Select dealer card 1 (A, 2-10, J, Q, K): ")


class BlackjackOddsStandHit(BlackjackOdds):
    def __init__(self, file_name):
        players = ["Hit", "Stand"]
        BlackjackOdds.__init__(self, players, file_name)

    def start_game(self, number_of_rounds=0):
        # Calculations must be done in a specific order, so that whenever an action after first action is required, it
        # has been created earlier.
        all_cards = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        # Hard 20...12 + soft 21
        for self.player_card_1_value in ["10"]:
            for self.player_card_2_value in all_cards:
                self.calculate_odds(all_cards, number_of_rounds)
        # Hard 11...2 and Soft 20...12 in turns
        for self.player_card_1_value in ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]:
            for self.player_card_2_value in ["A", "2"]:
                self.calculate_odds(all_cards, number_of_rounds)


class BlackjackOddsDoubleSplit(BlackjackOdds):
    def __init__(self, file_name):
        players = ["Double", "Split"]
        BlackjackOdds.__init__(self, players, file_name)

    def start_game(self, number_of_rounds=0):
        # TODO: Permutations can be reduced to save computational time
        all_cards = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        for self.player_card_1_value in all_cards:
            for self.player_card_2_value in all_cards:
                self.calculate_odds(all_cards, number_of_rounds)
