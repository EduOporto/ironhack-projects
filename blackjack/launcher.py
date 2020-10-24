import itertools
from random import shuffle

#FUNCTION THAT GENERATES A SHUFFLED LIST OF 52 TUPLES, EACH OF THOSE IS A (CARD NAME, VALUE) THAT ALTOGETHER MAKES A STANDARD DECK OF CARDS

def card_shuffler():
    card_val = [[('A',0)], [('J', 10), ('Q', 10), ('K', 10)], [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)]]
    suits = ['-C', '-D', '-H', '-S']

    card_deck = []
    for value in card_val:
        for i in value:
            for s in suits:
                card_w_suit = (i[0]+s,i[1])
                card_deck.append(card_w_suit)

    shuffle(card_deck)
    return card_deck

# CREATE A GENERATOR FUNCTION THAT YIELDS EACH OF THE LETTERS OF THE SHUFFLED DECK, SO THEY CAN BE ASSIGNED AMONG THE PLAYERS

def dealer(deck):
    for card in deck:
        yield card

# EACH PLAYER IS A KEY OF A DICTIONARY, EACH KEY AS A LIST AS A VALUE, AND THIS LIST RECIEVES THE CARDS THE DEALER IS DEALING

def set_table(n):
    table_dict = {'Dealer': []}
    num_players = list(range(1,n+1))

    for e in num_players:
        table_dict[f'Player{e}'] = []

    return table_dict


# NOW A FOR LOOP CAN GO AND ASSIGN CARDS IN ORDER TO THE DICT (TABLE): FIRST TO PLAYER 1, SECOND TO DEALER, THIRD TO PLAYER 1 ... AND SO ON UP TO EACH OF THE PLAYERS HAS TWO CARDS

deck = card_shuffler()
table = set_table(1) #THIS WILL VARY AS THE NUMBER OF PLAYERS VARY
deal_card = dealer(deck)
initial_deals = list(range(2)) #THIS COULD VARY AS THE NUMBER OF PLAYER VARY

for deal in initial_deals:
    for player in table:
        table[player].append(next(deal_card)) 

# AFTER THE LOOP EACH OF THE PLAYERS IN THE TABLE HAS TWO CARDS, NOW IS TIME TO ASK EACH OF THEM IF THEY WANT AN EXTRA CARD
    
