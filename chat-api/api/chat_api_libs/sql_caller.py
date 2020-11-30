from sqlalchemy import create_engine
from getpass import getpass
from dotenv import load_dotenv
import pandas as pd
import os
from random import choice

def engine_connector():
## Function that serves as a connector to the database
    load_dotenv()
    passwd = os.getenv('MySQLPass')

    mysql_url = f'mysql+mysqldb://root:{passwd}@localhost'
    engine = create_engine(mysql_url)
    
    return engine.connect()

## Call for the function above, in order to allow the rest of the functions connect with the database
conn = engine_connector()

def user_call(user, id=False, conn=conn):   
## Function that returns either the user_nick or the user_id when parameter id=True.
## Returns a message whenever the user plugged is not in the database
    try:
        if id == False:
            query = f"""SELECT user_nick, user_id
                FROM chat_api.users
                WHERE user_nick = '{user}';
                """
            res = pd.read_sql(con=conn, sql=query)

            return res['user_id'][0]
        elif id == True:
            query = f"""SELECT user_nick, user_id
                FROM chat_api.users
                WHERE user_id = '{user}';
                """
            res = pd.read_sql(con=conn, sql=query)

            return res['user_nick'][0]
    except:
        return f"User '{user}' not in the database. Please, register this user first"

def chat_checker(sender, receiver, chat_id=False, conn=conn):
## Function that returns either a chat_name or a chat_id when parameter chat_id=True, when the id's of two users are plugged
## Returns a message whenever the users plugged have no chat in common
## This function recognises users' chats in any position you plug them

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

def group_checker(group_name, sender_id, new_user, conn=conn):
## Function that check whether a new user can be added to a group or not

    try:
        query = f"""SELECT *
        FROM chat_api.users_has_groups
        WHERE group_name = '{group_name}';
        """
        res = pd.read_sql(con=conn, sql=query)  
            
        users_list = res.iloc[0,-4:].to_list()
        new_user_id = user_call(new_user)
            
        if sender_id == res['user_id_admin'][0] and new_user_id not in users_list and None in users_list:
        # If the admin has called the function, the new user is not already in the group and there is space the function returns a tuple
        # with the id of the group and the column where the new user will be added
            
            users = res.iloc[0,-4:]
            column = [index for index, value in users.iteritems() if value == None][0]
            return (res['group_id'][0], column)

        elif sender_id == res['user_id_admin'][0] and None not in users_list:
        # If the admin has called the function, but there is no space in the group the function returns a message  

            return f"Sorry, '{group_name}' group is full"

        elif sender_id == res['user_id_admin'][0] and new_user_id in users_list:
        # If the admin has called the function, but the new user is already in the group the function returns a message  
            
            return f"'{new_user}' is already in the group!"

        else:
        # If the user that is calling the function is not the admin of the group
            return "Invalid admin nick for this group"     
    
    except:
        # Just in case the name of the group plugged does not exists

        return f"Group '{group_name}' does not exists..."

def get_group_id(group_name, sender_id, conn=conn):
# This function returns the group id if the user that is calling it is in the group; otherwise returns a message

    query = f"""SELECT *
                FROM chat_api.users_has_groups
                WHERE group_name = '{group_name}';
            """
    res = pd.read_sql(con=conn, sql=query)

    users_list = res.iloc[0,-4:].to_list()

    if sender_id in users_list:
        return res['group_id'][0]
    else:
        return f"You cannot access to '{group_name}', as you are not in the group"


def get_chats(random_chat=False, conn=conn):
# This function returns either a dataframe with the list of chats saved in the Database or a randomly picked chat 

    query = f"""SELECT *
            FROM chat_api.users_has_chats"""

    df = pd.read_sql(con=conn, sql=query)

    if random_chat == False:
        return df
    elif random_chat == True:
        chats_list = df['chat_name'].to_list()
        return choice(chats_list)

def get_groups(random_group=False, con=conn):
# This function returns either a dataframe with the list of groups saved in the Database or a randomly picked group 

    query = f"""SELECT *
                FROM chat_api.users_has_groups"""

    df = pd.read_sql(con=conn, sql=query)

    if random_group == False:
        return df
    elif random_group == True:
        return df.sample()

def get_users(random_user=False, con=conn):
# This function returns either a dataframe with the list of users saved in the Database or a randomly picked user 

    query = f"""SELECT * 
                FROM chat_api.users;
            """
    
    df = pd.read_sql(con=conn, sql=query)

    if random_user == False:
        return df
    elif random_user == True:
        return df.sample()