from player import Player
from deck import Deck
from hand import Hand
from tkinter import *


class Blackjack():

    def __init__(self, players, dealer, gui=False, debugging=False, pcv=False, dcv=False):
        self.players = [Player(name) for name in players]
        self.dealer = Dealer(dealer)
        self.deck = Deck()
        self.number_of_decks = 6  # Typical number of decks in casinos
        self.rounds = 0
        if gui:
            self.gui = False  # TODO: GUI - graphics not working (28.2.2015 - JT)
        else:
            self.gui = False
        self.pcv = pcv
        self.dcv = dcv
        self.debugging = debugging

    def start_game(self, number_of_rounds):
        # TODO: GUI - set table graphics
        for _ in range(0, number_of_rounds):
            self.start_round()
        for player in self.players:
            for hand in player.get_hands():
                print(player.name, "käsi")
                hand.show_cards()
        print("JAKAJA")
        self.dealer.get_hand().show_cards()

        money = 0
        # Print results
        for player in self.players:
            player.show_money()
            # TODO: GUI - show money
            money += player.get_money()
        print("odds are for the house: ", (1000 - money/len(self.players))/number_of_rounds*100, "percent")

    def start_round(self):
        # Initialize players and (if needed) shuffle the deck
        if self.gui:
            self.frame = Frame(self.root)


        if self.deck.cards_left() < 30 or self.debugging == True:
            self.deck.shuffled(self.number_of_decks)
            # TODO: GUI - Show this event (animation)

        for player in self.players:
            player.new_round(ratio=self.deck.ratio / self.deck.cards_left()*52)
        self.dealer.new_round()

        # Deal two cards to each player and dealer.
        # TODO: cards are dealt in wrong order, but that doesn't change the odds.

        if self.debugging == False:
            for player in self.players * 2:
                for hand in player.get_hands():
                    self.deck.deal(1, hand)
            self.deck.deal(2, self.dealer.get_hand())
        else:
            # Deal two SPECIFIC cards to each player and the dealer - DEBUGGING
            for player in self.players:
                for hand in player.get_hands():
                    self.deck.deal_value_card(self.pcv[0], hand)  # TODO: check that dealing is ok by odds
                    self.deck.deal_value_card(self.pcv[1], hand)
            self.deck.deal_value_card(self.dcv, self.dealer.get_hand())
            self.deck.deal(1, self.dealer.get_hand())

        # Gameplay
        for player in self.players:
            self.player_turn(player)
        self.dealer_turn()

        # End game
        self.decide_winner()

    def player_turn(self, player, first_action=None):
        # http://www.wikihow.com/Sample/Blackjack-Rules
        # Default: use playbook/rulebook defined in class Player()
        # Optional: First action can be specified if default playbook/rulebook is not wanted.
        # - allowed terms for first_action: "Split", "Double", "Stay", "Hit"
        # - NOTE! user must make sure that given action is allowed.
        #   If action is illegal, player loses all money and discards hand!!! (needed for blackjack_odds)
        #   TODO: Try to make it so, that ACCIDENTAL illegal first_actions are handled
        # TODO: Error handling is very primitive
        while player.has_next_hand():  # A player is allowed to have multiple hands, especially with action == "Split".
            hand = player.next_hand()
            while True:
                if self.gui:  # TODO: GUI
                    self.frame.print_cards(turn="player")

                # DECIDE PLAYER ACTION
                if first_action is not None:  # Use the given action for first round and the playbook after that.
                    # TODO: check, should breaks be removed
                    if first_action == "Double" and not hand.can_double():  # Illegal action.
                        player.set_money(None)
                        player.discard(hand)
                        break
                    elif first_action == "Split" and not hand.can_split():  # Illegal action.
                        player.set_money(None)
                        player.discard(hand)
                        break
                    else:
                        action = first_action
                        first_action = None
                else:  # Use the default playbook/rulebook
                    try:
                        action = player.move(hand, self.dealer.hand)
                    except TypeError:  # FOR DEBUGGING
                        print("TypeError in player.move - something went wrong. Check blackjack.py")
                        break
                    except KeyError:  # FOR DEBUGGING
                        print("KeyError in player.move - something went wrong. Check blackjack.py")
                        # self.dealer.hand.showcards()
                        # print(hand.showcards())
                        break

                # EXECUTE ACTION
                if action == "Stand" or action == "Stay":
                    break
                elif action == "Hit":
                    self.deck.deal(1, hand)
                elif action == "Split":
                    if hand.can_split() is True:
                        player.split(hand)  # TODO: check that this works (and should both hands get card)
                        self.deck.deal(1, hand)
                    else:
                        # One should never find himself here
                        print("ERROR - player tried to do illegal split")
                        # hand.show_cards()
                        # print("ERROR ENDS")
                        break
                elif action == "Double" and hand.can_double:
                    hand.doublebet()
                    self.deck.deal(1, hand)
                    break  # after Double player has to take one card and stay.
                else:
                    # One should never find himself here
                    print("FAIL! action", action, "not found")
                    break

    def dealer_turn(self):
        while True:
            if self.gui:  # TODO: GUI
                self.frame.print_cards(turn="dealer")
            action = self.dealer.move()
            if action == "Stand":
                break
            elif action == "Hit":
                self.deck.deal(1, self.dealer.get_hand())

    def decide_winner(self):
        # http://www.wikihow.com/Sample/Blackjack-Rules
        if self.gui:  # TODO: GUI
            self.frame.print_cards(turn="dealer")
        dealer_hand = self.dealer.get_hand()
        for player in self.players:
            for hand in player.get_hands():
                if hand.sum_of_cards() > 21:  # Hand over, player loses
                    player.change_money(hand.lose())
                elif hand.is_blackjack() and not dealer_hand.is_blackjack():  # Player blackjack wins
                        player.change_money(hand.win(1.5))
                elif dealer_hand.is_blackjack() and not hand.is_blackjack():  # House blackjack wins
                        player.change_money(hand.lose())
                elif hand.sum_of_cards() == dealer_hand.sum_of_cards():  # Tie
                        player.change_money(hand.tie())
                elif dealer_hand.sum_of_cards() > 21:  # House over
                    player.change_money(hand.win())
                elif hand.sum_of_cards() > dealer_hand.sum_of_cards():  # Hand wins
                    player.change_money(hand.win())
                elif hand.sum_of_cards() < dealer_hand.sum_of_cards():  # House wins
                    player.change_money(hand.lose())
                else:
                    # One never is here, I hope
                    print("ERROR - unable to determine winner in: blackjack.py - decide_winner()")


class Dealer():  # TODO: move this to other file
    def __init__(self, name):
        self.name = name
        self.hand = None

    def new_round(self):
        self.hand = Hand()

    def move(self):
        if self.hand.sum_of_cards() <= 16:
            return "Hit"
        else:
            return "Stand"

    def get_hand(self):
        return self.hand



