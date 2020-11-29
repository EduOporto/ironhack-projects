from sqlalchemy import create_engine
from getpass import getpass
from dotenv import load_dotenv
import pandas as pd
import os

def engine_connector():
    load_dotenv()
    passwd = os.getenv('MySQLPass')

    mysql_url = f'mysql+mysqldb://root:{passwd}@localhost'
    engine = create_engine(mysql_url)
    
    return engine.connect()

def user_call(user_nick):
    conn = engine_connector()

    query = f"""SELECT user_nick, user_id
    FROM chat_api.users
    WHERE user_nick = '{user_nick}';
    """
    res = pd.read_sql(con=conn, sql=query)

    return res['user_id'][0]

def chat_checker(sender, receiver, chat_id=False):
    conn = engine_connector()

    query = f"""SELECT chat_id FROM chat_api.users_has_chats
                WHERE (user_id_send={sender} AND user_id_recv={receiver}) OR 
                (user_id_send={receiver} AND user_id_recv={sender});
            """

    if chat_id == False:
        return pd.read_sql(con=conn, sql=query).shape[0]
    elif chat_id == True:
        try:
            return pd.read_sql(con=conn, sql=query)['chat_id'][0]
        except:
            return "This chat does not exist!"

