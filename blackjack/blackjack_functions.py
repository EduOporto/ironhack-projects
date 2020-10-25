import itertools
from random import shuffle

# FUNCTION THAT GENERATES THE TABLE

def set_table(n_players):
    table = {'Dealer': []}
    for player in list(range(1,int(n_players)+1)):
        name = input(f"PLAYER_{player}, PLEASE,TELL ME YOUR NAME: ")
        print("\n")
        table[name] = []
    
    return table

#FUNCTION THAT GENERATES A SHUFFLED LIST OF 52 TUPLES, EACH OF THOSE IS A (CARD NAME, VALUE) THAT ALTOGETHER MAKES A STANDARD DECK OF CARDS

def card_shuffler():
    card_val = [[('A', 0)], [('J', 10), ('Q', 10), ('K', 10)], [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)]]
    suits = ['-C', '-D', '-H', '-S']

    card_deck = []
    for value in card_val:
        for i in value:
            for s in suits:
                card_w_suit = (i[0]+s,i[1])
                card_deck.append(card_w_suit)

    shuffle(card_deck)
    return card_deck

# CREATE A GENERATOR FUNCTION THAT YIELDS EACH OF THE CARDS OF THE SHUFFLED DECK, SO THEY CAN BE ASSIGNED AMONG THE PLAYERS

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

# FUNCTION THAT CHECKS OUT THE POINTS (AND CHOOSES WHETHER THE ACE IS 1 OR 11)

def points_checker(hand):
    points = [e[1] for e in hand]
    while 0 in points:
        points.remove(0)
        if sum(points) <= 10:
            points.append(11)
        else:
            points.append(1)
    
    return points

# NOW IS TIME TO SHOW THE TABLE STATUS

def status(table, dealer_shows=False):
    print("\n----------TABLE----------\n")
    if dealer_shows:
        cards_str = ""
        for card in table['Dealer']:
            cards_str += (card[0]+"/")
        print(f"Dealer: {cards_str}")
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
        acc = 0
        points = [acc+e[1] for e in table[player]]
        if 0 in points:
            points.remove(0)
            if sum(points) <= 10:
                points.append(11)
            else:
                points.append(1)
        else:
            pass

        if sum(points) == 21 and len(points) <= 3:
            table[player].append(('BLACKJACK!!', 0))
        elif sum(points) > 21:
            table[player].append(('LOSE...', 0))
        else:
            print("\n")
            choice = input(f"{player}, would you like another card?(y/n): ")
            if choice.lower() == 'y':
                more_deals.append(player)
                table[player].append(next(deal_card))
            else:
                pass
        
    return table, more_deals

# TURN FOR THE DEALER TO GET CARDS

def dealer_get(table, deal_card):
    acc = 0
    dealer_points = [acc+e[1] for e in table['Dealer']]
    
    dealer_extra_cards = 0
    
    while sum(dealer_points) < 17:
        dealer_extra_cards += 1
        while 0 in dealer_points:
            ace_index = dealer_points.index(0)
            if sum(dealer_points) <= 10:
                table['Dealer'][ace_index] = (table['Dealer'][ace_index][0], 11)
                dealer_points = [acc+e[1] for e in table['Dealer']]
            else:
                table['Dealer'][ace_index] = (table['Dealer'][ace_index][0], 1)
                dealer_points = [acc+e[1] for e in table['Dealer']]
        else:
            table['Dealer'].append(next(deal_card))
            dealer_points = [acc+e[1] for e in table['Dealer']]

    if dealer_extra_cards == 1:
        print(f"\nTHE DEALER NEEDED {dealer_extra_cards} MORE CARD")
    elif dealer_extra_cards == 0:
        print(f"\nTHE DEALER NEEDED NO MORE CARDS")
    else:
        print(f"\nTHE DEALER NEEDED {dealer_extra_cards} MORE CARDS")

    return table

# CHECK WINNERS, LOSERS AND DRAWS

def checker(table):
    blackjacks = []
    less_or_21 = []
    losers = []
    for player, hand in table.items():
        points = [e[1] for e in hand]
        if 0 in points:
            points.remove(0)
            if sum(points) <= 10:
                points.append(11)
            else:
                points.append(1)
        else:
            pass
        
        if sum(points) == 21 and len(points) <= 3:
            blackjacks.append((player, sum(points)))
        if sum(points) <= 21:
            less_or_21.append((player, sum(points)))
        else:
            losers.append((player, sum(points)))
    
    if len(blackjacks) > 0:
        print(f"\nBlackjacks: {[e[0] for e in blackjacks]}")
    else:
        if len(less_or_21) > 0:
            #less_or_21.sort(key= lambda x: x[1])
            print(f"\nWinners: {[e[0] for e in less_or_21]}")
        if len(losers) > 0:    
            print(f"\nLosers: {[e[0] for e in losers]}")

    
