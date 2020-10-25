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

# FUNCTION THAT GENERATES A SHUFFLED LIST OF 52 TUPLES, EACH OF THOSE IS A (CARD NAME, VALUE) THAT ALTOGETHER MAKES A STANDARD DECK OF CARDS

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

# GENERATOR FUNCTION THAT YIELDS EACH OF THE CARDS OF THE SHUFFLED DECK, SO THEY CAN BE ASSIGNED AMONG THE PLAYERS

def dealer(deck):
    for card in deck:
        yield card

# FUNCTION THAT ASSIGNS CARDS IN ORDER TO THE DICT (TABLE): FIRST TO PLAYER(S), THEN TO DEALER; SECOND CARD TO PLAYER(S), THEN TO DEALER

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
        if 150 in points:
            if sum(points)-150 <= 10:
                points.append(11)
            else:
                points.append(1)
        elif 100 in points:
            if sum(points)-100 <= 10:
                points.append(11)
            else:
                points.append(1)
        elif 50 in points:
            if sum(points)-50 <= 10:
                points.append(11)
            else:
                points.append(1)
        else:
            if sum(points) <= 10:
                points.append(11)
            else:
                points.append(1)

    return points

# FUNCTION THAT SHOWS THE TABLE STATUS

def status(table, dealer_shows=False):
    print("\n----------TABLE----------\n")
    if dealer_shows:
        cards_str = ""
        for card in table['Dealer']:
            cards_str += (card[0]+"/")
        print(f"Dealer: {cards_str}")
    else:
        print(f"Dealer: {table['Dealer'][0][0]}/**")
    
    more_deals = []
    for player in [e for e in table][1:]:
        points = points_checker(table[player])
        if 150 not in points and 100 not in points and 50 not in points:
            if sum(points) == 21 and len(points) <= 3:
                table[player].append(('BLACKJACK!!', 150))
            elif sum(points) > 21:
                table[player].append(('LOSE...', 100))
            else:
                more_deals.append(player)
        else:
            pass

        cards_str = ""
        for card in table[player]:
            cards_str += (card[0]+"/")
        print(f"{player}: {cards_str}")

    return more_deals

# ASK EACH OF THEM IF THEY WANT AN EXTRA CARD

def new_deal(table, players_to_ask, deal_card):
    for player in players_to_ask: 
        points = points_checker(table[player])
        
        if 150 not in points and 100 not in points:    
            print("\n")
            choice = input(f"{player}, would you like another card?(y/n): ")
            if choice.lower() == 'y':
                table[player].append(next(deal_card))
            if choice.lower() == 'n':
                if 50 not in points:
                    table[player].append(('PASS', 50))
                
    return table 

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
    dealer_points = sum(points_checker(table['Dealer']))
    for player in [e for e in table][1:]:
        player_points = [e[1] for e in table[player]]
        if 150 in player_points:
            player_points = 22
        elif 100 in player_points:
            player_points = 0
        elif 50 in player_points:
            player_points = sum(player_points)-50
        
        if player_points > dealer_points:
            print (f"{player} wins Dealer")
        elif player_points < dealer_points:
            print(f"Dealer wins {player}")
        else:
            print(f"{player} and Dealer draw")
