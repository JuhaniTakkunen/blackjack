from player import Player
from deck import Deck
from hand import Hand
from print_functions import *
from dealer import Dealer
from blackjack_ui import *
from blackjack_rules import BlackjackRules


class Blackjack(object):
    # print_ functions are imported from print_functions.py
    # ui_ functions are imported from blackjack_ui.py

    def __init__(self, players, counting=False, manual=False):
        self.players = [Player(name) for name in players]
        self.dealer = Dealer()
        self.deck = Deck()
        self.round_count = 0
        self.counting = counting
        self.manual = manual
        self.rules = BlackjackRules()

    def start_game(self, number_of_rounds=0):
        if self.manual:
            while True:
                continue_game = self.start_round()
                if not continue_game:
                    break
        else:
            for _ in range(0, number_of_rounds):
                self.start_round()
        print_results(players=self.players, rounds=self.round_count)

    def start_round(self):
        # Shuffle the deck (if needed)
        if self.deck.cards_left() < self.rules.cards_left_min:
            self.deck.shuffle_all(self.rules.number_of_decks)

        # Initialize players, bets and the dealer
        for player in self.players:
            if self.counting:
                player.new_round(self.deck.get_ratio())
            else:
                player.new_round()
        self.dealer.new_round()

        # Play the game, deal the cards etc.
        self.deal_initial()
        for player in self.players:
            self.player_turn(player)
        self.dealer_turn()

        # End game - solve winners, deal money and print what's needed
        self.round_count += 1
        self.rules.decide_winner(self)

        if self.manual:
            print_round_ended(self)
            print_player_round_stats(self)
            return ui_continue_game(self)

    def deal_initial(self):
            # Deal two cards to each player and dealer.
            # TODO: cards are dealt in wrong order, but that doesn't change the odds.
            for player in self.players * 2:
                for hand in player.get_hands():
                    self.deck.deal(1, hand)
            self.deck.deal(2, self.dealer.get_hand())

    def player_turn(self, player):
        # Default: use playbook/rulebook defined in class Player()
        # Optional: First action can be specified if default playbook/rulebook is not wanted.
        # - allowed terms for first_action: "Split", "Double", "Stay", "Hit"
        # - NOTE! user must make sure that given action is allowed.
        #   If action is illegal, player loses all money and discards hand!!! (needed for blackjack_odds)
        #   TODO: Try to make it so, that ACCIDENTAL illegal first_actions are handled
        # TODO: Error handling is very primitive
        if self.manual:
            print_player_turn(player)
        while player.has_next_hand():  # A player is allowed to have multiple hands, especially with action == "Split".
            hand = player.next_hand()
            while True:
                # 0. CHECK IF BUSTED
                if hand.sum_of_cards() > 21:
                    if self.manual:
                        print_busted(player, hand)
                    break

                # 1. GET ACTION
                action = self.get_action(player, hand)
                if not action:
                    break

                # 2. EXECUTE ACTION
                if action == "Stand" or action == "Stay":
                    break
                elif action == "Hit":
                    self.deck.deal(1, hand)
                elif action == "Split" and hand.can_split():
                    player.split(hand)
                    self.deck.deal(1, hand)
                elif action == "Double" and hand.can_double:
                    hand.doublebet()
                    self.deck.deal(1, hand)
                    if self.manual:
                        print_double(player, hand)
                    break  # after Double player has to take one card and stay.
                else:
                    raise RuntimeError("Player tried to do illegal action: "+action)

    def get_action(self, player, hand):
        if len(hand.cards) == 1:  # Happens after split TODO: move this bit of code to when split happens
            action = "Hit"
        elif self.manual:
            playbook_action = player.move(hand, self.dealer.hand)
            action = ui_player_action(player=player, hand=hand, game=self, default=playbook_action)
        elif hand.first_action is not None:
            # Use the given action for first round and the playbook after that.
            action = hand.first_action
            if self.rules.is_action_allowed(action=action, hand=hand):
                action = hand.first_action
                hand.first_action = None  # first action is only used for the very first  player action TODO: should first action be per hand or per round??!?
            else:
                player.set_money(None)
                player.discard(hand)
                return False
        else:  # Use the default playbook/rulebook
            action = player.move(hand, self.dealer.hand)
        return action

    def dealer_turn(self):
        while True:
            action = self.dealer.move(self.rules)
            if action == "Stand":
                break
            elif action == "Hit":
                self.deck.deal(1, self.dealer.hand)
