import blackjack_functions

# PRESENTATION
print("WELCOME TO OPORTO'S BLAKCJACK CASINO!\n")
players = str(input("PLEASE, TELL ME HOW MANY PEOPLE WOULD YOU BE PLAYING: "))
print("\n")

# SET TABLE (make it as a function)
table = {'Dealer': []}
for player in list(range(1,int(players)+1)):
    name = input(f"PLAYER_{player}, PLEASE,TELL ME YOUR NAME: ")
    print("\n")
    table[name] = []

print("PERFECT! YOUR TABLE IS READY, GOOD LUCK!")

# SHUFFLE THE DECK OF CARDS AND SET THE GENERATOR (DEALER) 
cards = blackjack_functions.card_shuffler()
deal_card = blackjack_functions.dealer(cards)

# RUN AND SHOW THE FIRST DEAL

table_first_d = blackjack_functions.first_dealt(table, int(players), deal_card)
blackjack_functions.status(table_first_d)

# RUN THE REST OF THE DEALS

new_deals = [e for e in table_first_d][1:]
table_rest_d, more_deals = blackjack_functions.new_deal(table_first_d, new_deals, deal_card)
blackjack_functions.status(table_rest_d)

while len(more_deals) > 0:
    table_rest_d, more_deals = blackjack_functions.new_deal(table_rest_d, more_deals, deal_card)
    if len(more_deals) > 0:
        blackjack_functions.status(table_rest_d)
    else:
        blackjack_functions.status(table_rest_d, dealer_shows=True)

