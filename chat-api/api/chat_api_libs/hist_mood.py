import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download("vader_lexicon")
import pandas as pd

def concater(df):
    df.reset_index(drop=True, inplace=True)

    sia = SentimentIntensityAnalyzer()

    feel_list = df['message'].apply(lambda x: sia.polarity_scores(x)).to_list()
    feel_df = pd.DataFrame(feel_list)
    message_feels = pd.concat([df, feel_df], axis=1)
    message_feels.drop(['compound'], axis=1, inplace=True)

    return message_feels