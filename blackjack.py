from player import Player
from deck import Deck
from hand import Hand


class Blackjack():

    def __init__(self, players, dealer):
        self.players = [Player(name) for name in players]
        self.dealer = Dealer(dealer)
        self.deck = Deck()
        self.number_of_decks = 6
        self.rounds = 0

    def start_game(self, number_of_rounds):
        for _ in range(0, number_of_rounds):
            self.start_round()

        # END OF ROUNDS
        for player in self.players:
            player.show_money()

    def start_round(self):
        for player in self.players:
            player.new_round()
        self.dealer.new_round()

        if self.deck.cards_left() < 30:
            self.deck.shuffled(self.number_of_decks)
        # Deal two cards to each player and dealer
        for player in self.players * 2:
            for hand in player.get_hands():
                self.deck.deal(1, hand)

        self.deck.deal(2, self.dealer.get_hand())  # cards are played in wrong order, but that doesnt change the odds

        # Gameplay
        for player in self.players:
            self.player_turn(player)
        self.dealer_turn()
        # End game
        self.decide_winner()

    def player_turn(self, player, first_action=None):
        dcard = self.dealer.hand.get_card_ranks(n_cards=1, show_royal=False)
        while player.has_next_hand():
            hand = player.next_hand()

            if first_action is not None:  # Try to do something differently, "off-the-rulebook"
                if first_action == "Double" and not hand.can_double():
                    player.set_money(None)
                    player.discard(hand)
                    break
                elif first_action == "Split" and not hand.can_split():
                    player.set_money(None)
                    player.discard(hand)
                    break
                else:
                    action = first_action
                    first_action = None
            else:  # Use the playbook/rulebook
                try:
                    action = player.move(hand, self.dealer.hand)
                except TypeError:  # FOR DEBUGGING
                    print("error starts here")
                    print(dcard[0])
                    break
                except KeyError:  # FOR DEBUGGING
                    print("WAAAT")
                    self.dealer.hand.showcards()
                    print(dcard)
                    print(hand.showcards())
                    break

            if action == "Stand":  # Stand
                break
            elif action == "Hit":  # Hit
                self.deck.deal(1, hand)
            elif action == "Split":
                if hand.can_split() is True:
                    player.split(hand)
                    self.deck.deal(1, hand)
                else:
                    # One should never find himself here
                    print("ERROR - player tried to do illegal split")
                    hand.show_cards()
                    print("ERROR ENDS")
                    break
            elif action == "Double" and hand.can_double:  # Double
                hand.doublebet()
                self.deck.deal(1, hand)
                break
            else:
                # One should never find himself here
                print(action)
                print("FAIL! action not found")
                print(hand.has_splitted())
                break

    def dealer_turn(self):
        while True:
            action = self.dealer.move()
            if action == "Stand":
                break
            elif action == "Hit":
                hand = self.dealer.get_hand()
                self.deck.deal(1, self.dealer.get_hand())

    def decide_winner(self):
        dealer_hand = self.dealer.get_hand()
        for player in self.players:
            for hand in player.get_hands():
                if hand.sum_of_cards() > 21:  # hand over
                    player.change_money(hand.lose())
                elif hand.is_blackjack() and not dealer_hand.is_blackjack():  # Player blackjack wins
                        player.change_money(hand.win(1.5))
                elif dealer_hand.is_blackjack() and not hand.is_blackjack():  # House blackjack wins
                        player.change_money(hand.lose())
                elif hand.sum_of_cards() == dealer_hand.sum_of_cards():  # Tie
                        player.change_money(hand.tie())
                elif dealer_hand.sum_of_cards() > 21:  # House over
                    player.change_money(hand.win())
                elif hand.sum_of_cards() > dealer_hand.sum_of_cards():  # hand wins
                    player.change_money(hand.win())
                elif hand.sum_of_cards() < dealer_hand.sum_of_cards():  # House wins
                    player.change_money(hand.lose())
                else:
                    # One never is here I hope
                    print("ERRORERROR")


class Dealer():
    def __init__(self, name):
        self.name = name
        self.hand = []

    def new_round(self):
        self.hand = Hand()

    def move(self):
        if self.hand.sum_of_cards() <= 16:
            return "Hit"
        else:
            return "Stand"

    def get_hand(self):
        return self.hand



