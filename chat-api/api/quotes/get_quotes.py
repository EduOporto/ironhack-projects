
## This library returns an iterator with more than 30,000 quotes from famous people

import pandas as pd 
from random import shuffle

def get_quotes():
    quotes_df = pd.read_csv('/Users/eduardooportoalonso/Documents/Cursos/Ironhack/datamad1020/ironhack-projects/chat-api/api/quotes/QUOTE.csv')
    quotes = quotes_df['quote'].to_list()
    shuffle(quotes)
    
    return iter(quotes)