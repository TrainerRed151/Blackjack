#!/usr/bin/env python

import random
import sys


def newDeck(n):
    d = []
    for i in range(n):
        for j in range(13):
            for k in range(4):
                d.append(j+1)

    return d
        

def getFromDeck(deck):
    #return deck.pop(0)
    return random.randint(1, 13)


def readyDeck(pl, ds, n):
    d = newDeck(n)
    d.remove(pl[0])
    d.remove(pl[1])
    d.remove(ds)
    random.shuffle(d)

    return d


def handValue(hand):
    if hand.count(1) > 0:
        hand1 = hand[:hand.index(1)] + (0,) + hand[hand.index(1)+1:]
        hand2 = hand
        
        value1 = 0
        value2 = 0
        for card in hand1:
            if card == 0:
                value1 += 11
            elif card > 10:
                value1 += 10
            else:
                value1 += card

        for card in hand2:
            if card == 0:
                value2 += 11
            elif card > 10:
                value2 += 10
            else:
                value2 += card

        if value1 > 21 and value2 <= 21:
            return value2
        elif value1 <= 21 and value2 > 21:
            return value1
        else:
            return max(value1, value2)


    value = 0
    for card in hand:
        if card > 10:
            value += 10
        else:
            value += card

    return value
            

def ev(pl, ds, n, decks):
    stand = hit = dd = 0
    deck = [1]
    for i in range(n):
        #deck = readyDeck(pl, ds, decks)
        stand += evHelper(deck, pl, ds, 0, 1)
        
        #deck = readyDeck(pl, ds, decks)
        hit += evHelper(deck, pl, ds, 1, 1)
        
        #deck = readyDeck(pl, ds, decks)
        dd += evHelper(deck, pl, ds, 2, 1)
    
    print("""%d,%d/%d (%d runs)
stand: %f
hit: %f
dd: %f""" % (pl[0], pl[1], ds, n, stand/sims, hit/sims, dd/sims))


def evTable(pl, ds, n, decks):
    stand = 0
    deck = [1]
    for i in range(n):
        stand += evHelper(deck, pl, ds, 0, 1)

    return stand/n


def evTableDD(pl, ds, n, decks):
    dd = 0
    deck = [1]
    for i in range(n):
        dd += evHelper(deck, pl, ds, 2, 1)

    return dd/n


def evHelper(deck, pl, ds, action, bet):
    if handValue(pl) > 21:
        return -bet
    
    if action == 0:
        return playDealer(deck, pl, ds, bet)
    
    c = getFromDeck(deck)
    if action == 2:
        return playDealer(deck, pl+(c,), ds, 2*bet)

    return max(evHelper(deck, pl+(c,), ds, 0, bet), evHelper(deck, pl+(c,), ds, 1, bet))


def playDealer(deck, pl, ds, bet):
    if handValue(pl) > 21:
        return -bet

    dealer = (ds, getFromDeck(deck))
    while handValue(dealer) < 17:
        dealer = dealer + (getFromDeck(deck),)

    plv = handValue(pl)
    dlv = handValue(dealer)
    if dlv > 21:
        return bet
    
    if plv > dlv:
        return bet
    elif plv < dlv:
        return -bet
    else:
        return 0




if __name__ == "__main__":
    #player = (int(sys.argv[1]), int(sys.argv[2]))
    #dealerShowing = int(sys.argv[3])
    #sims = int(sys.argv[4])
    #
    #ev(player, dealerShowing, sims, 6)

    ds = int(sys.argv[1])
    sims = int(sys.argv[2])

    print("\t2\t3\t4\t5\t6\t7\t8\t9\t10\tAce")
    for i in range(11, 1, -1):
        if i == 11:
            print("Ace\t", end="")
            i = 1
        else:
            print("""%d\t""" % (i), end="")

        for j in range(2, 12):
            if j == 11:
                j = 1
            print("""%.3f\t""" % (evTable((i, j), ds, sims, 1)), end="")
            #print("""%d,%d\t""" % (i, j), end="")
        
        print()

    print("\n\n\t2\t3\t4\t5\t6\t7\t8\t9\t10\tAce")
    for i in range(11, 1, -1):
        if i == 11:
            print("Ace\t", end="")
            i = 1
        else:
            print("""%d\t""" % (i), end="")

        for j in range(2, 12):
            if j == 11:
                j = 1
            print("""%.3f\t""" % (evTableDD((i, j), ds, sims, 1)), end="")
            #print("""%d,%d\t""" % (i, j), end="")
        
        print()
