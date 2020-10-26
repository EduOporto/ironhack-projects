# TURN FOR THE DEALER TO GET CARDS

def dealer_get(table, deal_card):
    dealer_extra_cards = 0
    dealer_points = [e[1] for e in table['Dealer']]
    
    while 0 in dealer_points or sum(dealer_points) < 17:
        zero_indexes = [index for index, item in enumerate(dealer_points) if item == 0]
        if len(zero_indexes) == 1:
            if (sum(dealer_points)+11) >= 17 and (sum(dealer_points)+11) <= 21:
                table['Dealer'][zero_indexes[0]][1] = 11
                table['Dealer'].append(['PASS', 50])
                print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
                return table
            elif (sum(dealer_points)+11) < 17:
                dealer_extra_cards += 1
                table['Dealer'].append(next(deal_card))
            elif (sum(dealer_points)+11) > 21:
                dealer_extra_cards += 1
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'].append(next(deal_card))
            dealer_points = [e[1] for e in table['Dealer']]
        
        elif len(zero_indexes) == 2:
            if (sum(dealer_points)+12) >= 17 and (sum(dealer_points)+12) <= 21:
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 11
                table['Dealer'].append(['PASS', 50])
                print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
                return table
            elif (sum(dealer_points)+12) < 17:
                dealer_extra_cards += 1
                table['Dealer'].append(next(deal_card))
            elif (sum(dealer_points)+12) > 21:
                dealer_extra_cards += 1
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 1
                table['Dealer'].append(next(deal_card))
            dealer_points = [e[1] for e in table['Dealer']]
        
        elif len(zero_indexes) == 3:
            if (sum(dealer_points)+13) >= 17 and (sum(dealer_points)+13) <= 21:
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 1
                table['Dealer'][zero_indexes[2]][1] = 11
                table['Dealer'].append(['PASS', 50])
                print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
                return table
            elif (sum(dealer_points)+13) < 17:
                dealer_extra_cards += 1
                table['Dealer'].append(next(deal_card))
            elif (sum(dealer_points)+13) > 21:
                dealer_extra_cards += 1
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 1
                table['Dealer'][zero_indexes[2]][1] = 1
                table['Dealer'].append(next(deal_card))
            dealer_points = [e[1] for e in table['Dealer']]
                
        elif len(zero_indexes) == 4:
            if (sum(dealer_points)+14) >= 17 and (sum(dealer_points)+14) <= 21:
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 1
                table['Dealer'][zero_indexes[2]][1] = 1
                table['Dealer'][zero_indexes[3]][1] = 11
                table['Dealer'].append(['PASS', 50])
                print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
                return table
            elif (sum(dealer_points)+14) < 17:
                dealer_extra_cards += 1
                table['Dealer'].append(next(deal_card))
            elif (sum(dealer_points)+14) > 21:
                dealer_extra_cards += 1
                table['Dealer'][zero_indexes[0]][1] = 1
                table['Dealer'][zero_indexes[1]][1] = 1
                table['Dealer'][zero_indexes[2]][1] = 1
                table['Dealer'][zero_indexes[3]][1] = 1
                table['Dealer'].append(next(deal_card))
            dealer_points = [e[1] for e in table['Dealer']]
        
        else:
            if sum(dealer_points) == 21 and len(dealer_points) <= 3:
                table['Dealer'].append(['BLACKJACK!!', 200])
                return table
            elif sum(dealer_points) >= 17 and sum(dealer_points) <= 21:
                print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
                table['Dealer'].append(['PASS', 50])
                return table
            elif sum(dealer_points) < 17:
                dealer_extra_cards += 1
                table['Dealer'].append(next(deal_card))
                dealer_points = [e[1] for e in table['Dealer']]
            elif sum(dealer_points) > 21:
                table['Dealer'].append(['LOSE', 100])
                return table
    
    if sum(dealer_points) == 21 and len(dealer_points) <= 3:
        table['Dealer'].append(['BLACKJACK!!', 200])
    elif sum(dealer_points) >= 17 and sum(dealer_points) <= 21:
        table['Dealer'].append(['PASS', 50])
    elif sum(dealer_points) > 21:
        table['Dealer'].append(['LOSE', 100])
    
    print(f"\nTHE DEALER GOT {dealer_extra_cards}-EXTRA CARDS")
    return table