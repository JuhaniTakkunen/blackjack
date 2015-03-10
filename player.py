from hand import Hand


class Player():

    def __init__(self, name, first_action=None):
        self.name = name
        self.money = 1000
        self.bet = 1
        self.hands = {}  # Hand(): Has hand ended (Stay / Over)
        self.first_action = first_action

        # counters
        self.round_count = 0
        self.win_count = 0
        self.tie_count = 0
        self.lose_count = 0
        self.blackjack_count = 0

        # Load rulebook on how to play each the BlackJack in each scenario
        import csv
        with open('Blackjack-chart.csv', 'rt', encoding="UTF-8") as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            dealercard = next(data, None)
            rulebook = {}
            for row in data:
                handrule = {}
                for i in range(1, len(dealercard)):
                    handrule[dealercard[i]] = row[i]
                rulebook[row[0]] = handrule
        self.rulebook = rulebook

    def new_round(self, *ratio):
        self.round_count += 1
        if ratio:
            if ratio > 2:
                self.bet = int(ratio)
            else:
                self.bet = 1
        hand = Hand(self.bet)
        hand.first_action = self.first_action
        self.hands = {hand: False}

    def discard(self, hand):
        del self.hands[hand]

    def show_money(self):
        print(self.name, "has", self.money, "€ after", self.round_count, "rounds")

    def get_money(self):
        return self.money

    def win(self, hand, rules):
        self.win_count += 1
        if hand.is_blackjack():
            self.blackjack_count += 1
            hand.bet = hand.bet * rules.blackjack_win_ratio
            self.money += hand.bet
        else:
            self.money += hand.bet
        hand.status = "win"

    def lose(self, hand):
        self.lose_count += 1
        self.money -= hand.bet
        hand.status = "lose"

    def tie(self, hand):
        self.tie_count += 1
        hand.status = "tie"

    def set_money(self, money):
        self.money = money

    def split(self, hand):
        new_hand = hand.split()
        self.hands[new_hand] = False

    def number_of_hands(self):
        return len(self.hands)

    def has_next_hand(self):
        for hand in self.hands:
            if not self.hands[hand]:
                return True
        return False

    def next_hand(self):
        for hand in self.hands:
            if not self.hands[hand]:
                self.hands[hand] = True
                return hand
        raise Exception("No playable hands")

    def get_hands(self):
        return self.hands

    def move(self, hand, dealer_hand):
        dealer_ranks = dealer_hand.get_card_ranks(n_cards=1, show_royal=False)
        player_ranks = hand.get_card_ranks(show_royal=False)
        if hand.can_split() is True:  # two cards with the same value
            search_word = str(player_ranks[0]) + ' ' + str(player_ranks[1])  # TODO: invent better variable name (search_word)
            action = self.rulebook[search_word][str(dealer_ranks[0])]  # csv-file format | TODO: rename rulebook -> playbook
        elif hand.has_ace() and hand.can_double():  # "soft" double has different odds than "hard"
            if player_ranks[0] is "A":
                search_word = str(player_ranks[0]) + ' ' + str(player_ranks[1])
            else:
                search_word = str(player_ranks[1]) + ' ' + str(player_ranks[0])
            action = self.rulebook[search_word][str(dealer_ranks[0])]
        else:
            points = hand.sum_of_cards()
            if points <= 8:
                points = "8 and under"
            elif points >= 17:
                points = "17 and up"
            else:
                points = str(points)

            try:
                action = self.rulebook[points][str(dealer_ranks[0])]
            except TypeError:
                print("FAIL in class Player function move")
                print(points, dealer_ranks[0])
                print("-------")
                print(self.rulebook)

        if action == "Double" and not hand.can_double():
            action = "Hit"
        elif action == "Split" and not hand.can_split():
            action = "Hit"
        return action