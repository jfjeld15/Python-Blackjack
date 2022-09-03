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
    numPlayers = 0
    print("Welcome to Blackjack!".center(88))
    print(("This is a very simple version of the game, so players can only 'hit' or 'stand'.").center(88))
    print(("No other moves may be played, and no additional bets can be made after the initial bets.").center(88))
    while numPlayers < 1 or numPlayers > 6:
        numPlayers = int(input("How many players will be playing (1-6)? "))
        if numPlayers < 1 or numPlayers > 6:
            print(("Please enter a value between 1 and 6.").center(88))
    i = 0
    while i < numPlayers:
        name = input("Enter player " + str(i+1) + "'s name: ")
        name = name.strip().lower().capitalize()  # We are polite. We capitalize our names.
        if name == "Dealer":
            print(("Please name yourself something else.").center(88))
            continue
        players[name] = Player()  # creates an object of class Player, stores it in dict players
        order.append(name)  # keeps track of player order (dictionaries are unordered)
        i += 1
    players["Dealer"] = Player()  # The dealer is also a Player object, for easier score-keeping.
    return players, order


def buildDeck():
    cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4  # initialize a 52-card deck
    random.shuffle(cards)  # shuffles the deck.
    return cards


def betDeal(who, when, cards):
    """ Players place their bets, and the cards are dealt for the round. Cards are removed from the deck
        as they are dealt, and scores are calculated for all players."""
    for name in when:
        betting = True
        while betting:
            bet = input(name + ', Place your bet (type "bal" to see your balance): ')
            if bet.lower().strip() == 'bal':
                print((name + " has " + str(who[name].bal) + " credits.").center(88))
            elif (int(bet) > who[name].bal) or (int(bet) <= 0):
                print(("Invalid credits bet! Please bet between 0 and " + str(who[name].bal) + " credits.").center(88))
            elif (int(bet) < who[name].bal) and (int(bet) > 0):
                who[name].bal -= int(bet)
                who[name].bet = int(bet)
                betting = False  # The player has successfully made a bet
            else:
                print(("Invalid response.").center(88))
        print((name + " has bet " + str(who[name].bet) + " credits.").center(88))
    # Betting has been completed. Now the dealer will deal to the players in order.
    for i in range(2):  # all players (and the dealer) are dealt 2 cards
        for name in when:
            who[name].hand.append(cards.pop(0))  # removes it from the deck, gives it to the player.
            who[name].score = count(who[name])  # add score
        who["Dealer"].hand.append(cards.pop(0))  # removes it from the deck, gives it to the dealer.
        who["Dealer"].score = count(who["Dealer"])
    return who, cards


def count(player):
    """ Counts the player's total score. Aces are counted last to determine if they are 1 or 11. This numerical score
        is never displayed to the player."""
    total = 0
    comeback = 0
    for card in player.hand:
        if card not in ['A','J','Q','K']:
            total += int(card)
        elif card in ['J','Q','K']:
            total += 10
        else:
            # The card is an ace. This is tricky.
            comeback += 1  # We must count the other cards first to decide if this is a 1 or 11.
    if comeback > 0:
        for i in range(comeback):
            if (total + 11) <= 21:
                total += 11  # We try to add 11 first.
            elif (total + 1) <= 21:
                total += 1
            else:
                # if neither are <=21, the player has busted! It should not matter what is added.
                total += 1
    return total


def showTable(who, when):
    # Displays all face up cards on the "table".
    print(("----The face-up cards for each player are:----").center(88))
    print(("----DEALER: [" + who["Dealer"].hand[0] + ", ???]----").center(88))
    for name in when:
        if who[name].score > 21:
            print(("----" + name + ": " + str(who[name].hand) + " (BUST!)----").center(88))
        else:
            print(("----" + name + ": " + str(who[name].hand) + "----").center(88))


def playGame(who, when, cards):
    """ Players take turns. They may only hit or stand."""
    for name in when:
        playing = True
        while playing:
            ans = input(name + ", will you hit or stand? (type 'h', 's', or 'view' to view the table): ")
            if ans.lower().strip() == "s":
                playing = False
            elif ans.lower().strip() == "h":
                who[name].hand.append(cards.pop(0))  # removes it from the deck, gives it to the player.
                who[name].score = count(who[name])  # add score
                if who[name].score > 21:
                    print(("----" + name + ": " + str(who[name].hand) + "----").center(88))
                    print(("You busted!").center(88))
                    playing = False
                else:
                    print(("----" + name + ": " + str(who[name].hand) + "----").center(88))
            elif ans.lower().strip() == "view":
                showTable(who, when)
            else:
                print(("Invalid Response.").center(88))
    print(("----All Players have played----").center(88))
    playing = True
    while playing:
        print(("Dealer's hand: " + str(who["Dealer"].hand)).center(88))
        who["Dealer"].score = count(who["Dealer"])
        if who["Dealer"].score < 17:
                    print(("The dealer hits").center(88))
                    who["Dealer"].hand.append(cards.pop(0))  # removes it from the deck, gives it to the dealer.
                elif who["Dealer"].score >= 17 and who["Dealer"].score <= 21:
                    print(("The dealer stands.").center(88))
                    playing = False
if __name__ == "__main__":
    players, order = startGame()
    deck = buildDeck()
    players, deck = betDeal(players, order, deck)
    showTable(players, order)
    playGame(players, order, deck)
    