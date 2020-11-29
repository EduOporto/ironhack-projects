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
    try:
        conn = engine_connector()

        query = f"""SELECT user_nick, user_id
        FROM chat_api.users
        WHERE user_nick = '{user_nick}';
        """
        res = pd.read_sql(con=conn, sql=query)

        return res['user_id'][0]
    except:
        return f"User '{user_nick}' not in the database. Please, register this user first"

def chat_checker(sender, receiver, chat_id=False):
    conn = engine_connector()

    query = f"""SELECT chat_id FROM chat_api.users_has_chats
                WHERE (user_id_send={sender} AND user_id_recv={receiver}) OR 
                (user_id_send={receiver} AND user_id_recv={sender});
            """

    if chat_id == False:
        try:
            return pd.read_sql(con=conn, sql=query).shape[0]
        except:
            return "This chat does not exist!"
    elif chat_id == True:
        try:
            return pd.read_sql(con=conn, sql=query)['chat_id'][0]
        except:
            return "This chat does not exist!"

def group_checker(group_name, sender_id, check_admin=False, check_space=False):
    conn = engine_connector()

    try:
        query = f"""SELECT *
        FROM chat_api.users_has_groups
        WHERE group_name = '{group_name}';
        """
        res = pd.read_sql(con=conn, sql=query)

        if check_admin == True and check_space == True:
            if sender_id == res['user_id_admin'][0] and None in res.iloc[0,-4:].to_list():
                users = res.iloc[0,-4:]
                column = [index for index, value in users.iteritems() if value == None][0]
                return (res['group_id'][0], column)
            elif sender_id == res['user_id_admin'][0] and None not in res.iloc[0,-4:].to_list():
                return f"Sorry, '{group_name}' group is full"
            else:
                return "Invalid admin nick for this group"     
        elif check_admin == False and check_space == False:
            if sender_id in res.iloc[0,-4:].to_list():
                return res['group_id'][0]
            else:
                return f"You cannot access to '{group_name}', as you are not in the group"
    except:
        return f"Group '{group_name}' does not exists..."