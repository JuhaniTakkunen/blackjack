from blackjack import Blackjack
import time


class BlackjackOdds(Blackjack):
    def deal_initial(self):
        self.deck.shuffle_new(self.rules.number_of_decks)  # every round is a "new" round  TODO: this cancels card counting
        for player in self.players:
            for hand in player.get_hands():
                self.deck.deal_value_card(self.player_card_1_value, hand, self.keep_in_deck)  # TODO: check that dealing is ok by odds
                self.deck.deal_value_card(self.player_card_2_value, hand, self.keep_in_deck)
        self.deck.deal_value_card(self.dealer_card_value, self.dealer.get_hand())
        self.deck.shuffle_rest()
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds


class BlackjackOddsSpecificAuto(Blackjack):

    def __init__(self, hand, dealer_hand):
        self.keep_in_deck = True
        players = ["Stand", "Hit", "Double", "Split"]
        Blackjack.__init__(self, players)
        self.hand = hand
        self.dealer_hand = dealer_hand

    def deal_initial(self):
        self.deck.shuffle_all(self.rules.number_of_decks)  # every round is a "new" round  TODO: this cancels card counting
        for player in self.players:
            for hand in player.get_hands():
                for card in self.hand.cards:
                    self.deck.deal_value_card(card.rank, hand, self.keep_in_deck)  # TODO: check that dealing is ok by odds
        for card in self.dealer_hand.cards:
            dealer_card_value = card.rank  #only the first card # TODO: do we need for loop for this
            break
        self.deck.deal_value_card(dealer_card_value, self.dealer.get_hand())
        self.deck.shuffle_rest()
        self.deck.deal(1, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds


class BlackjackOddsSpecificManual(BlackjackOdds):

    def __init__(self, player):
        self.keep_in_deck = False
        Blackjack.__init__(self, player)
        self.player_card_1_value = input("Select player card 1 (A, 2-10, J, Q, K): ")
        self.player_card_2_value = input("Select player card 2 (A, 2-10, J, Q, K): ")
        self.dealer_card_value = input("Select dealer card 1 (A, 2-10, J, Q, K): ")


class BlackjackOddsAll(BlackjackOdds):
    # Odds if we have infinite decks
    def __init__(self, file_object):
        players = ["Stand", "Hit", "Double", "Split"]
        Blackjack.__init__(self, players)
        for player in self.players:
            player.default_first_action = player.name
        self.file_object = file_object
        self.player_card_1_value = ""
        self.player_card_2_value = ""
        self.dealer_card_value = ""
        self.start_money = 1000
        self.rules.number_of_decks = 8
        self.keep_in_deck = True

    def start_game(self, number_of_rounds):
        start_time = time.time()
        all_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]
        i = 0
        for self.player_card_1_value in all_cards:
            i += 1
            for self.player_card_2_value in all_cards:
                for self.dealer_card_value in all_cards:
                    for player in self.players:
                        player.set_money(self.start_money)
                    for _ in range(0, number_of_rounds):  # TODO: parallelisation
                        self.start_round()
                    self.print_results_to_file(number_of_rounds)
            elapsed_time = time.time() - start_time
            done_str = "done at " + time.strftime("%H:%M:%S")
            elap_str = "time elapsed: " + str("{0:.2f}".format(elapsed_time)) + "s"
            est_str = "remaining: " + str("{0:.2f}".format(elapsed_time*len(all_cards) / i - elapsed_time)) + "s"
            print(self.player_card_1_value, done_str, elap_str, est_str)
        print("ALL DONE IN ", "{0:.2f}".format(time.time()-start_time), "seconds")

    def print_results_to_file(self, number_of_rounds):
        print(self.player_card_1_value, self.player_card_2_value, "\t", end="\t", file=self.file_object)
        print(self.dealer_card_value, end="\t", file=self.file_object)
        for player in self.players:
            try:
                money = str("{:3.4f}".format((player.get_money()-self.start_money)/number_of_rounds))
            except TypeError:
                money = " None "
            print(money, end="\t", file=self.file_object)
        print("", file=self.file_object)


class BlackjackOddsStandHit(BlackjackOdds):
    def __init__(self, file_name):
        players = ["Hit", "Stand"]
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

    def start_game(self, number_of_rounds):
        all_cards = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]
        # Hard 20...12 + soft 21
        for self.player_card_1_value in ["10"]:
            for self.player_card_2_value in all_cards:
                for self.dealer_card_value in all_cards:
                    for player in self.players:
                        player.set_money(self.start_money)
                        player.update_playbook()
                    for _ in range(0, number_of_rounds):
                        self.start_round()
                    self.print_results_to_file(number_of_rounds)

        # Hard 11...2 and Soft 20...12 in turns
        for self.player_card_1_value in ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]:
            for self.player_card_2_value in ["A", "2"]:
                for self.dealer_card_value in all_cards:
                    for player in self.players:
                        player.set_money(self.start_money)
                        player.update_playbook()
                    for _ in range(0, number_of_rounds):  # TODO: parallelisation
                        self.start_round()
                    self.print_results_to_file(number_of_rounds)

    def print_results_to_file(self, number_of_rounds):

        if self.player_card_1_value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            prefix = "Hard"
            sum_of_cards = int(self.player_card_1_value)
        elif self.player_card_1_value == "A":
            prefix = "Soft"
            sum_of_cards = 11

        if self.player_card_2_value == "A":
            sum_of_cards += 11
            prefix = "Soft"
            if sum_of_cards == 22:
                sum_of_cards = 12
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


class BlackjackOddsDoubleSplit(BlackjackOdds):
    def __init__(self, file_name):
        players = ["Double", "Split"]
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

    def start_game(self, number_of_rounds):

        all_cards = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "A"]

        for self.player_card_1_value in all_cards:
            for self.player_card_2_value in all_cards:
                for self.dealer_card_value in all_cards:
                    for player in self.players:
                        player.set_money(self.start_money)
                    for _ in range(0, number_of_rounds):  # TODO: Parallelisation
                        self.start_round()
                    self.print_results_to_file(number_of_rounds)

    def print_results_to_file(self, number_of_rounds):

        if self.player_card_1_value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            prefix = "Hard"
            sum_of_cards = int(self.player_card_1_value)
        elif self.player_card_1_value == "A":
            prefix = "Soft"
            sum_of_cards = 11

        if self.player_card_2_value == "A":
            sum_of_cards += 11
            prefix = "Soft"
            if sum_of_cards == 22:
                sum_of_cards = 12
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