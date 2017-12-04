import cs50
import sys
import random

def deal(deck):
    hand = []
    for i in range(2):
	    random.shuffle(deck)
	    card = deck.pop()
	    if card == 11:
	    	card = "J"
	    if card == 12:
	    	card = "Q"
	    if card == 13:
	    	card = "K"
	    if card == 1:
	    	card = "A"
	    hand.append(card)
    # print(hand) used during testing
    return hand

def wager():
    print("Please wager your bet. Minimum bet is 1 coin. Maximum bet is 10 coins.")
    bet = cs50.get_int()
    if bet < 1 or bet > 10:
    	print("You entered an invalid quantity.")
    	wager()
    return bet

def score(hand):
	L = len(hand)
	for i in range(L-1):
		if hand[i] == "A":
			hand[i] = hand[L-1]
			hand[L-1] = "A"
	score = 0
	for i in range(L):
		if hand[i] == "J" or hand[i] == "Q" or hand[i] == "K":
			score += 10
		elif hand[i] == "A" and (score + 11 <= 21):
			score += 11
		elif hand[i] == "A" and (score + 11 > 21):
			score += 1
		else:
			score += hand[i]
	# print("Your score is {}".format(score)) used during testing
	return score

def hit(hand, deck):
	card = deck.pop()
	if card == 11:
		card = "J"
	if card == 12:
		card = "Q"
	if card == 13:
		card = "K"
	if card == 1:
		card = "A"
	print("A(n) {} was drawn.".format(card))
	hand.append(card)
	return hand

def compare(player_scoreA, dealer_score):
    if player_scoreA > dealer_score:
        print("Player's {} beats dealer's {}. You win!".format(player_scoreA, dealer_score))
        winnings = 1
    if player_scoreA < dealer_score:
        print("Player's {} loses to dealer's {}. Dealer wins.".format(player_scoreA, dealer_score))
        winnings = -1
    if player_scoreA == dealer_score:
        print("Player and dealer has the same score of {}. Push".format(player_scoreA))
        winnings = 0 # no bets are won or lost in a push
    return winnings