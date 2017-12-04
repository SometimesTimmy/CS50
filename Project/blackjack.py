import cs50
import sys
import os

from helpers import *

def first_game():
    print("Welcome to single-deck Blackjack! You will start the game with 100 coins.")
    coin = 100
    game(coin)

def game(coin):
    bet = wager()
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]*4
    print("Dealer has shuffled the deck.")
    player_hand = deal(deck)
    dealer_hand = deal(deck)

    # provide player with information about his/her own hand and reveal one of the dealer's cards
    print("Your hand: {}".format(player_hand))
    print("Dealer is showing {}".format(dealer_hand[1]))

    # confirm if dealer has a blackjack
    # this results in an auto-win for the dealer unless the player also has a black jack
    if dealer_hand[1] == "A":
        if score(player_hand) == 21:
            print("Do you wish to take a 1:1 win instead of 1.5? Y or N: ", end="")
            normal_win = cs50.get_string()
            if normal_win == Y:
                coin += bet
                print("You now have {} coins".format(coin))
                new_game(coin)

        # player may surrender and lose half the bet when an ace is showing on the dealer's face-up card
        print("Do you wish to surrender half your bet? Y or N: ", end="")
        surrender = cs50.get_string()
        if surrender == "Y":
            coin -= bet*0.5
            print("You now have {} coins".format(coin))
            new_game(coin)

        # if the player choose to not surrender, the dealer must truthly reveal whether or not the dealer has blackjack
        elif surrender == "N":
            dealer_score = score(dealer_hand)
            if dealer_score == 21:
                print("Dealer has blackjack. Dealer wins.")
                coin -= bet
                print("You now have {} coins".format(coin))
                new_game(coin)
            if dealer_score < 21:
                print("Dealer found to not have blackjack. Player's turn")

    # split logic not yet implmented

    # player is awarded 1.5 times the bet for a blackjack
    if score(player_hand) == 21:
        print("Congratulation! You got a Blackjack!")
        coin += bet*1.5
        print("You now have {} coins".format(coin))
        new_game(coin)

    finish = 0 # zero indicates player has not doubled down or decided to stand
    while score(player_hand) <= 20:
        print("Would you like to [H]it, [D]ouble-down, [S]tand, or [Q]uit: ", end="")
        decision = cs50.get_string()
        if decision == "H":
            hit(player_hand, deck)
            player_score = score(player_hand)
            print("Your score is {}.".format(player_score))
        # doubling down will double the initial bet, but the player may only draw 1 card
        elif decision == "D":
            bet += bet
            hit(player_hand, deck)
            player_score = score(player_hand)
            print("Your score is {}.".format(player_score))
            break
        elif decision == "S":
            player_score = score(player_hand)
            print("Your score is {}.".format(player_score))
            break
        else: # or Q
            exit()
    if player_score > 21:
        print("Oh no! You busted! Dealer wins")
        coin -= bet
        print("You now have {} coins".format(coin))
        new_game(coin)

    print("It is now dealer's turn. Dealer's hand is revealead to be: {}".format(dealer_hand))
    dealer_score = score(dealer_hand)
    print("Dealer's score is {}.".format(dealer_score))
    while score(dealer_hand) < 17:
        hit(dealer_hand, deck)
        dealer_score = score(dealer_hand)
        print("Dealer's score is {}.".format(dealer_score))
        if dealer_score > 21:
            print("Dealer busted! You win!")
            coin += bet
            print("You now have {} coins".format(coin))
            new_game(coin)

    for i in range(len(dealer_hand)):
        if dealer_hand[i] == "A" and score(dealer_hand) == 17:
            print("Dealer hits on a soft 17")
            hit(dealer_hand, deck)
            while score(dealer_hand) < 17:
                hit(dealer_hand, deck)
                dealer_score = score(dealer_hand)
                print("Dealer's score is {}.".format(dealer_score))
    winnings = compare(player_score, dealer_score) # compare will look at the two hands and output 1, -1, or 0
    # future variant to include splits in compare
    coin += bet*winnings
    print("You now have {} coins".format(coin))
    new_game(coin)

def new_game(coin):
    print("Do you wish to start a new game? Y or N: ", end="")
    new = cs50.get_string()
    if new == "Y":
	    dealer_hand = []
	    player_hand = []
	    game(coin) # game is defined in blackjack.py
    else:
    	print("Thank you for playing. You reached {} coins.".format(coin)) # coin is defined in blackjack.py
    	sys.exit()

if __name__ == "__main__":
    first_game()