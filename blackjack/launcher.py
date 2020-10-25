import blackjack_functions

# PRESENTATION
print("WELCOME TO OPORTO'S BLAKCJACK CASINO!\n")
players = str(input("PLEASE, TELL ME HOW MANY PEOPLE WOULD YOU BE PLAYING: "))
print("\n")
table = blackjack_functions.set_table(players)

print("PERFECT! YOUR TABLE IS READY, GOOD LUCK!")

# SHUFFLE THE DECK OF CARDS AND SET THE GENERATOR (DEALER) 
cards = blackjack_functions.card_shuffler()
deal_card = blackjack_functions.dealer(cards)

# RUN AND SHOW THE FIRST DEAL

table_first_d = blackjack_functions.first_dealt(table, int(players), deal_card)
new_deals = blackjack_functions.status(table_first_d)

# RUN THE REST OF THE DEALS

#new_deals = [e for e in table_first_d][1:]
table_rest_d = blackjack_functions.new_deal(table_first_d, new_deals, deal_card) # TAKE OUT THIS ARGUMENT/VARIABLE ----> , new_deals / , more_deals
more_deals = blackjack_functions.status(table_rest_d)

while len(more_deals) > 0:
    table_rest_d = blackjack_functions.new_deal(table_rest_d, more_deals, deal_card) # TAKE OUT THIS ARGUMENT/VARIABLE ----> , new_deals / , more_deals
    more_deals = blackjack_functions.status(table_rest_d)

print("\nTHE DEALER SHOWS ITS HAND...\n")
blackjack_functions.status(table_rest_d, dealer_shows=True)

# TURN FOR THE DEALER TO GET CARDS

table_with_dealer = blackjack_functions.dealer_get(table_rest_d, deal_card)
blackjack_functions.status(table_with_dealer, dealer_shows=True)

# CHECK BLACKJACKS, WINNERS, LOSERS

blackjack_functions.checker(table_with_dealer)