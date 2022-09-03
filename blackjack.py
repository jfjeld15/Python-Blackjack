# Jonathan Fjeld, 2022
# Designing a simple game of Blackjack using Python.

# The purpose of this project is to remember basic Python syntax, classes, and good coding practices.

import random


class Player:
    # Default player class. This is updated as players play the game.
    def __init__(self):
        self.hand = []  # Player starts with an empty hand
        self.bal = 500 # starting balance
        self.score = 0 # score (out of 21)
        self.bet = 0 # what the player bets on the current game


def startGame():
    # Prompts the user to input number of players, and creates an object of class Player for each player, stored in dict players.
    players = {}  # dictionary of players
    order = []  # order of players
    numPlayers = int(input("How many players will be playing (1-6)? "))
    for i in range(numPlayers):
        name = input("Enter player " + str(i+1) + "'s name: ")
        name.capitalize()  # We are polite. We capitalize our names.
        players[name] = Player()  # creates an object of class Player, stores it in dict players
        order.append(name)  # keeps track of player order (dictionaries are unordered)
    return players, order


def buildDeck():
    cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4  # initialize a 52-card deck
    random.shuffle(cards)  # shuffles the deck.
    return cards


def betDeal(who, when, cards):
    # Players place their bets, and the cards are dealt for the round.
    for name in when:
        betting = True
        while betting:
            bet = input(name + ', Place your bet (type "bal" to see your balance): ')
            if bet.lower().strip() == 'bal':
                print(name + " has " + str(who[name].bal) + " credits.")
            elif (int(bet) > who[name].bal) or (int(bet) <= 0):
                print("Invalid credits bet! Please bet between 0 and " + str(who[name].bal) + " credits.")
            elif (int(bet) < who[name].bal) and (int(bet) > 0):
                who[name].bal -= int(bet)
                who[name].bet = int(bet)
                betting = False  # The player has successfully made a bet
            else:
                print("Invalid response.")
        print(name + " has bet " + str(who[name].bet) + " credits.")
    # Betting has been completed. Now the dealer will deal to the players in order.
    for name in when:
        
    return who

if __name__ == "__main__":
    players, order = startGame()
    deck = buildDeck()
    players = betDeal(players, order, deck)
    