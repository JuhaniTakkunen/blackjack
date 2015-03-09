__author__ = 'Juhani Takkunen'
from tkinter import *
# NOT IN USE!!

class start_gui():
    def __init__(self, root):
        self.root = root

    def get_players(self):
        frame = Frame(self.root)
        frame.pack()
        players = []
        def return_players():
            frame.quit()

        players_default = ["Jenni", "Veikko", "Junnu", "Matti"]

        print("Get players:")
        label_player1 = Label(frame, text="player 1 name")
        label_player2 = Label(frame, text="player 2 name")
        label_player3 = Label(frame, text="player 3 name")

        entry_1 = Entry(frame)
        entry_2 = Entry(frame)
        entry_3 = Entry(frame)

        # defaults
        entry_1.insert(10, players_default[0])
        entry_2.insert(10, players_default[1])
        entry_3.insert(10, players_default[2])


        label_player1.grid(row=0, sticky=E)
        label_player2.grid(row=1, sticky=E)
        label_player3.grid(row=2, sticky=E)

        entry_1.grid(row=0, column=1)
        entry_2.grid(row=1, column=1)
        entry_3.grid(row=2, column=1)

        button = Button(frame, text="OK", command=return_players)
        button.grid(row=4, column=1, sticky=E)

        frame.mainloop()

        players = (entry_1.get(), entry_2.get(), entry_3.get())
        frame.destroy()

        return players


    def get_dealer(self):
        frame = Frame(self.root)
        frame.pack()
        dealer = []
        def return_dealer():
            frame.quit()

        print("Get dealer")
        dealer_default = "Teemu"

        label_dealer = Label(frame, text="dealer name")

        entry_1 = Entry(frame)
        entry_1.insert(10, dealer_default)


        label_dealer.grid(row=0, sticky=E)

        entry_1.grid(row=0, column=1)

        button = Button(frame, text="OK", command=return_dealer)
        button.grid(row=4, column=1, sticky=E)

        frame.mainloop()

        dealer = entry_1.get()
        frame.destroy()

        return dealer

    def print_cards(self, turn):
        if turn == "player":
            # print cards on table, only one for the dealer
            print("print not implemented")
        elif turn == "dealer":
            # print cards on the table, show all dealer cards
            print("print not implemented")
        else:
            print("please specify, dealer or player (blackjack_gui.print_cards()")