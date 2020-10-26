# FUNCTION THAT ASSIGNS CARDS IN ORDER TO THE DICT (TABLE): FIRST TO PLAYER(S), THEN TO DEALER; SECOND CARD TO PLAYER(S), THEN TO DEALER

def first_dealt(table, n_deals, dealer):
    initial_deals = list(range(2))

    for deal in initial_deals:
        for player in table:
            table[player].append(next(dealer))

    return table

# ASK EACH OF THEM IF THEY WANT AN EXTRA CARD

def new_deal(table, players_to_ask, deal_card):
    for player in players_to_ask: 
        points = points_checker(table[player])
        
        if 200 not in points and 150 not in points and 100 not in points:    
            print("\n")
            choice = input(f"{player}, would you like another card?(y/n): ")
            if choice.lower() == 'y':
                table[player].append(next(deal_card))
            if choice.lower() == 'n':
                #if 50 not in points:
                table[player].append(['PASS', 50])
                
    return table 

# FUNCTION THAT CHECKS OUT THE POINTS (AND CHOOSES WHETHER THE ACE IS 1 OR 11)

def points_checker(hand):
    points = [e[1] for e in hand]
    while 0 in points:
        points.remove(0)
        if 200 in points:
            if sum(points)-200 <= 10:
                points.append(11)
            else:
                points.append(1)
        elif 150 in points:
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

# CHECK WINNERS, LOSERS AND DRAWS

def checker(table):
    results = []
    for player in [e for e in table]:
        points = [e[1] for e in table[player]]
        if 200 in points:
            points = 22
        elif 150 in points:
            points = 21
        elif 100 in points:
            points = 0
        elif 50 in points:
            points = sum(points)-50
        else:
            points = sum(points)
        results.append((player, points))
    
    dealer_points = results[0][1]
    for player in [e for e in results][1:]:
        if player[1] > dealer_points:
            print (f"\n{player[0]} wins Dealer")
        elif player[1] < dealer_points:
            print(f"\nDealer wins {player[0]}")
        else:
            print(f"\n{player[0]} and Dealer draw")
