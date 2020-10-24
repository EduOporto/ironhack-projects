import blackjack_functions

# PRESENTATION
print("WELCOME TO OPORTO'S BLAKCJACK CASINO!\n")
players = str(input("PLEASE, TELL ME HOW MANY PEOPLE WOULD YOU BE PLAYING: "))

# SET TABLE
table = {'Dealer': []}
for player in list(range(1,int(players)+1)):
    name = input(f"PLAYER_{player}, PLEASE,TELL ME YOUR NAME: ")
    table[name] = []

print("PERFECT! YOUR TABLE IS READY, GOOD LUCK!")

# SHUFFLE THE DECK OF CARDS AND SET THE GENERATOR (DEALER) 
cards = blackjack_functions.card_shuffler()
deal_card = blackjack_functions.dealer(cards)

# RUN THE FIRST DEAL

table_first_d = blackjack_functions.first_dealt(table, int(players), deal_card)

print(table_first_d)



