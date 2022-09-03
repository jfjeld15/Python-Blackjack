# Jonathan Fjeld, 2022
# Attempting to recreate a simple game of 1-on-1 Blackjack using Python.

# The purpose of this project is to remember basic Python syntax, classes.

import random

deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4  # initialize a 52-card deck
dealer = []  # Dealer's hand
players = {}  # dictionary of players


class Player:
    def __init__(self):
        self.hand = []  # Player starts with an empty hand
        self.bal = 500 # starting balance
        self.score = 0 # score (out of 21)
        self.bet = 0 # what the player bets on the current game

def startGame():
    # Prompts the user to input number of players, and creates an object of class Player for each player, stored in dict players.
    numPlayers = int(input("How many players will be playing (1-6)? "))
    for i in range(numPlayers):
        name = input("Enter player " + str(i+1) + "'s name: ")
        players[name] = Player()  # creates an object of class player, stores it in dictionary


if __name__ == "__main__":
    startGame()
    