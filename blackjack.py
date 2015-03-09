from player import Player
from deck import Deck
from hand import Hand
# blackjack.py defines the rules of blackjack and how the game should be played. Blackjack rules have multiple
# variations, and here we use the following rules:
# - dealer hits on 16 stands on 17
# - money returns to player in case of tie
# - blackjack pays 3:2
# - hand can be split only once
# - double is not allowed for split hands
# - double can be done, if first two cards have a value in range of 9-11 # TODO: check this


class Blackjack(object):

    def __init__(self, players, dealer, counting=False, manual=False):
        self.players = [Player(name) for name in players]
        self.dealer = Dealer(dealer)
        self.deck = Deck()
        self.number_of_decks = 6  # Typical number of decks in casinos
        self.rounds = 0
        self.counting = counting
        self.manual = manual

    def start_game(self, number_of_rounds=0):
        if self.manual:
            continue_game = True
            while continue_game:
                continue_game = self.start_round()
        else:
            for _ in range(0, number_of_rounds):
                self.start_round()

        self.print_results()

    def start_round(self):
        # Initialize players and (if needed) shuffle the deck
        if self.deck.cards_left() < 30:
            self.deck.shuffle_all(self.number_of_decks)

        for player in self.players:
            if self.counting:
                player.new_round(self.deck.get_ratio())
            else:
                player.new_round()
        self.dealer.new_round()

        self.deal_initial()

        # Gameplay
        for player in self.players:
            self.player_turn(player)
        self.dealer_turn()

        # End game
        self.rounds += 1
        self.decide_winner()

        if self.manual:
            while True:
                var = input("Do you want to continue? [y/n]")
                if var == "y" or var == "Y":
                    return True
                elif var == "n" or var == "N":
                    return False
                else:
                    print("Please answer y or n.")

    def deal_initial(self):
            # Deal two cards to each player and dealer.
            # TODO: cards are dealt in wrong order, but that doesn't change the odds.
            for player in self.players * 2:
                for hand in player.get_hands():
                    self.deck.deal(1, hand)
            self.deck.deal(2, self.dealer.get_hand())

    def player_turn(self, player, first_action=None):
        # http://www.wikihow.com/Sample/Blackjack-Rules
        # Default: use playbook/rulebook defined in class Player()
        # Optional: First action can be specified if default playbook/rulebook is not wanted.
        # - allowed terms for first_action: "Split", "Double", "Stay", "Hit"
        # - NOTE! user must make sure that given action is allowed.
        #   If action is illegal, player loses all money and discards hand!!! (needed for blackjack_odds)
        #   TODO: Try to make it so, that ACCIDENTAL illegal first_actions are handled
        # TODO: Error handling is very primitive
        if self.manual:
            print("\n ---- Player", player.name, "turn! ---- \n")
        while player.has_next_hand():  # A player is allowed to have multiple hands, especially with action == "Split".
            hand = player.next_hand()
            while True:
                if hand.sum_of_cards() > 21:
                    if self.manual:
                        print(" ---- Player", player.name, "busted with", hand.sum_of_cards(), "points. ---- ")
                    break
                # 1. DECIDE PLAYER ACTION
                if len(hand.cards) == 1:  # Happens after split
                    action = "Hit"
                elif self.manual:
                    while True:
                        print("Player", player.name, hand.sum_of_cards(), "points: ")
                        hand.show_cards()
                        print("Dealer cards: ")
                        self.dealer.hand.show_cards(1)
                        text = "Choose action [hit, stay"
                        if hand.can_double():
                            text += ", double"
                        if hand.can_split():
                            text += ", split"
                        var = input(text+"]: ")
                        if var == "Split" or var == "split":
                            if hand.can_split():
                                action = "Split"
                                break
                            else:
                                print(" - sorry, split not allowed, choose another action.")
                        elif var == "Stay" or var == "stay" or var == "Stand" or var == "stand":
                            action = "Stay"
                            break
                        elif var == "Hit" or var == "hit":
                            action = "Hit"
                            break
                        elif var == "Double" or var == "double":
                            if hand.can_double():
                                action = "Double"
                                break
                            else:
                                print(" - sorry, double not allowed, choose another action.")
                        else:
                            print("- Invalid action, allowed actions are: split, stay, hit or double.")
                elif first_action is not None:  # Use the given action for first round and the playbook after that.
                    # TODO: check, should breaks be removed
                    if first_action == "Double" and not hand.can_double():  # Illegal action.
                        player.set_money(None)
                        player.discard(hand)
                        print("Player tried to do illegal split")
                        break
                    elif first_action == "Split" and not hand.can_split():  # Illegal action.
                        player.set_money(None)
                        player.discard(hand)
                        print("Player tried to do illegal split")
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

                # 2. EXECUTE ACTION
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
                    if self.manual:
                        print("Player", player.name, "stays after double with", end="")
                        hand.show_cards()
                        print("\n")
                    break  # after Double player has to take one card and stay.
                else:
                    # One should never find himself here
                    print("FAIL! action", action, "not found")
                    break

    def dealer_turn(self):
        while True:
            action = self.dealer.move()
            if action == "Stand":
                break
            elif action == "Hit":
                self.deck.deal(1, self.dealer.hand)

    def decide_winner(self):
        # http://www.wikihow.com/Sample/Blackjack-Rules
        dealer_hand = self.dealer.hand
        if self.manual:
            print("Round ended")
            print("Dealer hand", dealer_hand.sum_of_cards(), "points: ", end="")
            dealer_hand.show_cards()
        for player in self.players:
            for hand in player.get_hands():
                if hand.sum_of_cards() > 21:
                    player.lose(hand)
                elif dealer_hand.sum_of_cards() > 21:
                    player.win(hand)
                elif hand.is_blackjack() and not dealer_hand.is_blackjack():  # Player blackjack wins
                    player.win(hand)
                elif dealer_hand.is_blackjack() and not hand.is_blackjack():  # House blackjack wins
                    player.lose(hand)
                elif hand.sum_of_cards() == dealer_hand.sum_of_cards():  # Tie, important that we check blackjacks first
                    player.tie(hand)
                elif hand.sum_of_cards() > dealer_hand.sum_of_cards():
                    player.win(hand)
                elif hand.sum_of_cards() < dealer_hand.sum_of_cards():
                    player.lose(hand)
                else:
                    # One never is here, I hope
                    print("ERROR - unable to determine winner in: blackjack.py - Blackjack.decide_winner()")
                    print("Player", player.name, "cards: ")
                if self.manual:
                    print("Player", player.name, hand.status, hand.bet, "€ with", hand.sum_of_cards(), "points: ", end="")
                    hand.show_cards()

    def print_results(self):
        print("")
        print("--- *** RESULTS *** ---")
        print("")
        total_win_count, total_lose_count, total_tie_count, total_money_count = 0, 0, 0, 0

        for player in self.players:
            player.show_money()
            odds = (1000 - player.get_money())/self.rounds*100
            print("odds are for the house: ", odds, "percent")
            print("wins", player.win_count, "lost", player.lose_count, "tie", player.tie_count)
            print("")
            total_win_count += player.win_count
            total_lose_count += player.lose_count
            total_tie_count += player.tie_count
            total_money_count += player.get_money()

        print("--- combined results ---")
        odds = (1000*len(self.players) - total_money_count)/(self.rounds*len(self.players))*100
        print("odds are for the house: ", odds, "percent")
        print("wins", total_win_count, "lost", total_lose_count, "tie", total_tie_count)
        print("")


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
