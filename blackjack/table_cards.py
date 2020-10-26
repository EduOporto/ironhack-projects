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
    card_val = [[['A', 0]], [['J', 10], ['Q', 10], ['K', 10]], [['2', 2], ['3', 3], ['4', 4], ['5', 5], ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]]]
    suits = ['-C', '-D', '-H', '-S']

    card_deck = []
    for value in card_val:
        for i in value:
            for s in suits:
                card_w_suit = [i[0]+s,i[1]]
                card_deck.append(card_w_suit)

    shuffle(card_deck)
    return card_deck

# GENERATOR FUNCTION THAT YIELDS EACH OF THE CARDS OF THE SHUFFLED DECK, SO THEY CAN BE ASSIGNED AMONG THE PLAYERS

def dealer(deck):
    for card in deck:
        yield card