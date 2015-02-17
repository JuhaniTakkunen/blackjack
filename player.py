from hand import Hand


class Player():

    def __init__(self, name, action=None):
        self.name = name
        self.money = 1000
        self.bet = 1
        self.hands = {}  # Hand(): Has hand ended (Stay / Over)
        self.rounds = 0
        self.action = action

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

    def new_round(self):
        self.hands = {Hand(): False}
        self.rounds += 1

    def discard(self, hand):
        del self.hands[hand]

    def show_money(self, arg):
        if arg == "action":
            print(self.action,  "has", self.money, "€ after", self.rounds, "rounds")
        else:
            print(self.name,    "has", self.money, "€ after", self.rounds, "rounds")

    def get_money(self):
        return self.money

    def change_money(self, change):
        self.money += change

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
        if hand.can_split() is True:
            search_word = str(player_ranks[0]) + ' ' + str(player_ranks[1])  # TODO: invent better variable name (search_word)
            action = self.rulebook[search_word][str(dealer_ranks[0])]  # csv-file format | TODO: rename rulebook -> playbook
        elif hand.has_ace() and hand.can_double():
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

        if action == "Double" and hand.has_splitted():  # TODO: This should be unnecessary - is it safe to remove it?
            action = "Hit"
        return action