import table_cards
import deals_checker
import status
import dealer_behaviour

# PRESENTATION
print("WELCOME TO OPORTO'S BLAKCJACK CASINO!\n")
players = str(input("PLEASE, TELL ME HOW MANY PEOPLE WOULD YOU BE PLAYING: "))
print("\n")
table = table_cards.set_table(players)

print("PERFECT! YOUR TABLE IS READY, GOOD LUCK!")

# SHUFFLE THE DECK OF CARDS AND SET THE GENERATOR (DEALER) 
cards = table_cards.card_shuffler()
deal_card = table_cards.dealer(cards)

# RUN AND SHOW THE FIRST DEAL

table_first_d = deals_checker.first_dealt(table, int(players), deal_card)
new_deals = status.status(table_first_d)

# RUN THE REST OF THE DEALS

#new_deals = [e for e in table_first_d][1:]
table_rest_d = deals_checker.new_deal(table_first_d, new_deals, deal_card) # TAKE OUT THIS ARGUMENT/VARIABLE ----> , new_deals / , more_deals
more_deals = status.status(table_rest_d)

while len(more_deals) > 0:
    table_rest_d = deals_checker.new_deal(table_rest_d, more_deals, deal_card) # TAKE OUT THIS ARGUMENT/VARIABLE ----> , new_deals / , more_deals
    more_deals = status.status(table_rest_d)

print("\nTHE DEALER SHOWS ITS HAND...\n")
status.status(table_rest_d, dealer_shows=True)

# TURN FOR THE DEALER TO GET CARDS

table_with_dealer = dealer_behaviour.dealer_get(table_rest_d, deal_card)
status.status(table_with_dealer, dealer_shows=True)

# CHECK BLACKJACKS, WINNERS, LOSERS

deals_checker.checker(table_with_dealer)
#print(table_with_dealer)