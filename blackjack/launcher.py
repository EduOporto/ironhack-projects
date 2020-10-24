import itertools
from random import shuffle

#FUNCTION THAT GENERATES A SHUFFLED LIST OF 52 TUPLES, EACH OF THOSE IS A (CARD NAME, VALUE) THAT ALTOGETHER MAKES A STANDARD DECK OF CARDS

def card_shuffler():
    card_val = [[('A',0)], [('J', 10), ('Q', 10), ('K', 10)], [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)]]
    suits = ['-C', '-D', '-H', '-S']

    card_set = []
    for value in card_val:
        for i in value:
            for s in suits:
                card_w_suit = (i[0]+s,i[1])
                card_set.append(card_w_suit)

    return card_set
