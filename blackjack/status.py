from deals_checker import points_checker

# FUNCTION THAT SHOWS THE TABLE STATUS

def status(table, dealer_shows=False):
    print("\n----------TABLE----------\n")
    if dealer_shows:
        dealer_points = points_checker(table['Dealer'])
        cards_str = ""
        for card in table['Dealer']:
            cards_str += (card[0]+"/")
        print(f"Dealer: {cards_str}")
    else:
        print(f"Dealer: {table['Dealer'][0][0]}/**")
    
    more_deals = []
    for player in [e for e in table][1:]:
        points = points_checker(table[player])
        if 200 not in points and 150 not in points and 100 not in points and 50 not in points:
            if sum(points) == 21 and len(points) <= 3:
                table[player].append(['BLACKJACK!!', 200])
            if sum(points) == 21 and len(points) > 3:
                table[player].append(['TWENTY-ONE', 150])
            elif sum(points) > 21:
                table[player].append(['LOSE...', 100])
            else:
                more_deals.append(player)
        else:
            pass

        cards_str = ""
        for card in table[player]:
            cards_str += (card[0]+"/")
        print(f"{player}: {cards_str}")

    return more_deals