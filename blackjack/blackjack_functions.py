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


# NOW A FOR LOOP CAN GO AND ASSIGN CARDS IN ORDER TO THE DICT (TABLE): FIRST TO PLAYER 1, SECOND TO DEALER, THIRD TO PLAYER 1 ... AND SO ON UP TO EACH OF THE PLAYERS HAS TWO CARDS

def first_dealt(table, n_deals, dealer):
    initial_deals = list(range(2))

    for deal in initial_deals:
        for player in table:
            table[player].append(next(dealer))

    return table

# NOW IS TIME TO SHOW THE TABLE STATUS

def status(table, dealer_shows=False):
    print("\n----------TABLE----------\n")
    if dealer_shows:
        print(f"Dealer: {table['Dealer'][0][0]}/{table['Dealer'][0][0]}")
    else:
        print(f"Dealer: {table['Dealer'][0][0]}/**")
    
    for player in [e for e in table][1:]:
        cards_str = ""
        for card in table[player]:
            cards_str += (card[0]+"/")
        print(f"{player}: {cards_str}")

# ASK EACH OF THEM IF THEY WANT AN EXTRA CARD

def new_deal(table, players_to_ask, deal_card):
    more_deals = []
    for player in players_to_ask:
        print("\n")
        choice = input(f"{player}, would you like another card?(y/n): ")
        if choice.lower() == 'y':
            more_deals.append(player)
            table[player].append(next(deal_card))
        else:
            pass
        
    return table, more_deals


    
