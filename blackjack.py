# Jonathan Fjeld, 2022
# Designing a simple game of Blackjack using Python.

# The purpose of this project is to remember basic Python syntax, classes, and good coding practices.

from distutils.core import setup
import random
import time


class Player:
    # Default player class. This is updated as players play the game.
    def __init__(self):
        self.hand = []  # Player starts with an empty hand
        self.bal = 500  # starting balance
        self.score = 0  # score (out of 21)
        self.bet = 0  # what the player bets on the current game
        self.bust = False  # set to true if the player busts


def startGame():
    # Prompts the user to input number of players, and creates an object of class Player for each player, stored in dict players.
    who = {}  # dictionary of players
    when = []  # order of players
    numPlayers = 0
    print("- - - - - Welcome to Blackjack! - - - - -".center(88))
    time.sleep(0.3)
    print(("This is a very simple version of the game, so players can only 'hit' or 'stand'.").center(88))
    time.sleep(0.3)
    print(("No other moves may be played, and no additional bets can be made after the initial bets.").center(88))
    time.sleep(1)
    while numPlayers < 1 or numPlayers > 6:
        try:
            numPlayers = int(input("How many players will be playing (1-6)? "))
        except ValueError:
            print(("Please enter a value between 1 and 6.").center(88))
        else:
            if numPlayers < 1 or numPlayers > 6:
                print(("Please enter a value between 1 and 6.").center(88))
    i = 0
    while i < numPlayers:
        name = input("Enter player " + str(i+1) + "'s name: ")
        name = name.strip().lower().capitalize()  # We are polite. We capitalize our names.
        if name == "Dealer" or name in when:
            print(("Please name yourself something else.").center(88))
            continue
        who[name] = Player()  # creates an object of class Player, stores it in dict players
        when.append(name)  # keeps track of player order (dictionaries are unordered)
        i += 1
    who["Dealer"] = Player()  # The dealer is also a Player object, for easier score-keeping.
    return who, when


def buildDeck():
    cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4  # initialize a 52-card deck
    random.shuffle(cards)  # shuffles the deck.
    return cards


def betDeal(who, when, cards):
    """ Players place their bets, and the cards are dealt for the round. Cards are removed from the deck
        as they are dealt, and scores are calculated for all players."""
    who["Dealer"].hand = []  # reset the dealers hand in case it is not the first game.
    who["Dealer"].bust = False
    for name in when:
        who[name].hand = []  # reset any players hands who continued from a previous game
        who[name].bust = False
        betting = True
        while betting:
            bet = input(name + ', Place your bet (type "bal" to see your balance): ')
            try:
                if bet.lower().strip() == 'bal':
                    print((name + " has " + str(who[name].bal) + " credits.").center(88))
                elif (int(bet) > who[name].bal) or (int(bet) <= 0):
                    print(("Invalid credits bet! Please bet between 1 and " + str(who[name].bal) + " credits.").center(88))
                elif (int(bet) <= who[name].bal) and (int(bet) > 0):
                    who[name].bal -= int(bet)
                    who[name].bet = int(bet)
                    betting = False  # The player has successfully made a bet
            except ValueError:
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
            print(("----" + name + "'s hand: " + str(who[name].hand) + "----").center(88))
            ans = input(name + ", will you hit or stand? (type 'h', 's', or 'v' to view the table): ")
            if ans.lower().strip() == "s":
                print((name + " stands.").center(88))
                playing = False
            elif ans.lower().strip() == "h":
                who[name].hand.append(cards.pop(0))  # removes it from the deck, gives it to the player.
                who[name].score = count(who[name])  # add score
                if who[name].score > 21:
                    print(("----" + name + "'s hand: " + str(who[name].hand) + "----").center(88))
                    print((name + " busts!").center(88))
                    who[name].bust = True
                    playing = False
                else:
                    # They have not busted yet. Prompt another move.
                    continue
            elif ans.lower().strip() == "v":
                showTable(who, when)
            else:
                print(("Invalid Response.").center(88))
    print(("----All Players have played----").center(88))
    time.sleep(1)
    playing = True
    while playing:
        print(("Dealer's hand: " + str(who["Dealer"].hand)).center(88))
        time.sleep(1)
        who["Dealer"].score = count(who["Dealer"])
        if who["Dealer"].score < 17:
            print(("The dealer hits").center(88))
            who["Dealer"].hand.append(cards.pop(0))  # removes it from the deck, gives it to the dealer.
            time.sleep(1)
        elif who["Dealer"].score >= 17 and who["Dealer"].score <= 21:
            print(("The Dealer stands.").center(88))
            time.sleep(1)
            playing = False
        else:
            # The dealer has busted.
            print(("The Dealer busts!").center(88))
            who["Dealer"].bust = True
            time.sleep(1)
            playing = False
    return who  # I do not need to return the deck, as all players have played.


def payout(who, when):
    # Compares players scores with the dealer's score, and updates player balances.
    print(("- - - - - PAYOUT - - - - -").center(88))
    time.sleep(1)
    for name in when:
        if who[name].bust == False and who["Dealer"].bust == False:
            # Both the player and the dealer did not bust. Compare their scores.
            if who[name].score > who["Dealer"].score and who[name].score == 21:
                # The player has a Blackjack
                print(("Blackjack! " + name + " receives " + str(2.5*who[name].bet) + " credits.").center(88))
                who[name].bal += 2.5*who[name].bet
            elif who[name].score > who["Dealer"].score:
                # Not a blackjack, but the player still won
                print((name + " receives " + str(2*who[name].bet) + " credits.").center(88))
                who[name].bal += 2*who[name].bet
            elif who[name].score == who["Dealer"].score:
                # Nobody wins, the money is returned
                print(("Draw. " + name + " is returned " + str(who[name].bet) + " credits.").center(88))
                who[name].bal += who[name].bet
            elif who[name].score < who["Dealer"].score:
                # The dealer wins. No money is returned.
                print(("Dealer wins! Try again, " + name + ".").center(88))
        elif who[name].bust == False and who["Dealer"].bust == True:
            # The Dealer busted, and the player did not.
            print((name + " receives " + str(2*who[name].bet) + " credits.").center(88))
            who[name].bal += 2*who[name].bet
        else:
            # The player busts. Dealer wins.
            print((name + " busted! Try again, " + name + ".").center(88))
        time.sleep(1)
    return who


def playAgain(who, when):
    """ Displays all players balances, and gives some free credits to players who have reached 0.
        Players are then prompted to play again, reset the game, or exit."""
    removeList = []
    print(("- - - - - PLAYER BALANCES - - - - -").center(88))
    for name in when:
        print((name + " has " + str(who[name].bal) + " credits.").center(88))
    time.sleep(1)
    for name in when:
        answering = True
        while answering:
            if who[name].bal == 0:
                # The player has no balance, they can restart with 100.
                ans = input(name + ", keep playing with 100 credits? (type 'y' or 'n'): ")
                if ans.lower().strip() == "y":
                    print((name + " will continue playing.").center(88))
                    who[name].bal = 100
                    answering = False
                elif ans.lower().strip() == 'n':
                    print((name + " has been removed from the game.").center(88))
                    removeList.append(name)
                    answering = False
                else:
                    print(("Invalid Response.").center(88))
            else:
                ans = input(name + ", keep playing? (type 'y' or 'n'): ")
                if ans.lower().strip() == "y":
                    print((name + " will continue playing.").center(88))
                    answering = False
                elif ans.lower().strip() == "n":
                    print((name + " has been removed from the game.").center(88))
                    removeList.append(name)
                    answering = False
                else:
                    print(("Invalid Response.").center(88))
    for name in removeList:
        # The next 2 lines remove players who have quit.
        when.remove(name)
        who.pop(name)
    if len(when) == 0:
        # All players have quit. Endgame is set to true.
        return True, False, who, when
    else:
        answering = True
        print(("- - - - - Play Again? - - - - -").center(88))
        while answering:
            print(("To play again with players " + str(when) + ", type 'y'.").center(88))
            print(("To add more players, type 'a'.").center(88))
            print(("To quit, type 'q'.").center(88))
            ans = input()
            if ans == "y":
                answering = False
                return False, False, who, when
            elif ans == "a":
                if len(when) == 6:
                    print(("There are too many players to add more.").center(88))
                else:
                    who, when = addPlayers(who, when)
            elif ans == "q":
                answering = False
                return True, False, who, when
            else:
                print(("Invalid Response.").center(88))


def addPlayers(who, when):
    numAdd = 6
    maxAdd = 6 - len(when)  # Maximum number of players who can join
    while numAdd < 1 or numAdd > maxAdd:
        try:
            numAdd = int(input("How many players will be added (1-" + str(maxAdd) + ")? "))
        except ValueError:
            print(("Please enter a value between 1 and " + str(maxAdd) + ".").center(88))
        else:
            if numAdd < 1 or numAdd > maxAdd:
                print(("Please enter a value between 1 and " + str(maxAdd) + ".").center(88))
    i = 0
    while i < numAdd:
        name = input("Enter player " + str(len(when)+1) + "'s name: ")
        name = name.strip().lower().capitalize()  # We are polite. We capitalize our names.
        if name == "Dealer" or name in when:
            print(("Please name yourself something else.").center(88))
            continue
        who[name] = Player()  # creates an object of class Player, stores it in dict players
        when.append(name)  # keeps track of player order (dictionaries are unordered)
        i += 1
    return who, when


if __name__ == "__main__":
    endGame = False
    setupGame = True
    while endGame == False:
        if setupGame == True:
            players, order = startGame()
            setupGame = False
        deck = buildDeck()
        players, deck = betDeal(players, order, deck)
        showTable(players, order)
        players = playGame(players, order, deck)
        players = payout(players, order)
        endGame, setupGame, players, order = playAgain(players, order)
    print(("Thanks for playing!").center(88))
    