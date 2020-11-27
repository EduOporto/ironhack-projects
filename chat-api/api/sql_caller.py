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