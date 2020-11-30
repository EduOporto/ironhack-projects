from app import app
from flask import request
from bson import json_util
from sql_caller import engine_connector, user_call, chat_checker, group_checker
import numpy as np
from datetime import datetime
from string_fixer import string_fixer
import pandas as pd
import json

## Endpoints

## GENERALS ##

@app.route('/new_user')
def new_user():
    user_name = request.args.get('user_name')
    user_surname = request.args.get('user_surname')
    user_nick = request.args.get('user_nick')
    conn = engine_connector()

    query = f"""INSERT INTO chat_api.users (user_name, user_lastname, user_nick)
    VALUES ('{user_name}', '{user_surname}', '{user_nick}');
    """
    conn.execute(query)

    return f"{user_nick} succesfully added to our databases"

@app.route('/user_hist')
def user_hist():
    user_nick = request.args.get('user_nick')
    user_id = user_call(user_nick)

    conn = engine_connector()

    query_chats = f"""SELECT 
                        chat_id AS id,
                        chat_name AS name
                      FROM chat_api.users_has_chats
                      WHERE user_id_send = {user_id} OR user_id_recv = {user_id}
                  """

    query_groups = f"""SELECT 
                            group_id AS id,
                            group_name AS name
                       FROM chat_api.users_has_groups
                       WHERE user_id_admin = {user_id} OR 
                             user_1_id = {user_id} OR 
                             user_2_id = {user_id} OR 
                             user_3_id = {user_id}
                   """

    res_chats = pd.read_sql(con=conn, sql=query_chats)
    res_chats['name'] = res_chats['name'].apply(lambda x: x.replace(user_nick, '').replace('-', ''))
    res_chats.insert(1, 'type', 'chat')
    
    res_groups = pd.read_sql(con=conn, sql=query_groups)
    res_groups.insert(1, 'type', 'group')

    res = pd.concat([res_chats, res_groups], ignore_index=True).to_json(date_format='iso', force_ascii=True)
    
    return json.loads(res)

## CHATS ##

@app.route('/chat/create')
def new_chat():
    sender_nick = request.args.get('sender_nick') 
    receiver_nick = request.args.get('recv_nick')
    
    user_id_send = user_call(sender_nick)
    user_id_recv = user_call(receiver_nick)

    if chat_checker(user_id_send, user_id_recv) == 0:

        conn = engine_connector()

        query = f"""INSERT INTO chat_api.users_has_chats (chat_name, user_id_send, user_id_recv)
        VALUES ('{sender_nick}-{receiver_nick}', '{user_id_send}', '{user_id_recv}');
        """
        conn.execute(query)

        return f"Chat between {sender_nick} and {receiver_nick} succesfully added to our databases"

    else:
        return f"Chat between {sender_nick} and {receiver_nick} already exists!"

@app.route('/chat/addmessage')
def add_message():
    sender_nick = request.args.get('sender_nick')
    receiver_nick = request.args.get('recv_nick')
    message = request.args.get('message')

    user_id_send = user_call(sender_nick)
    user_id_recv = user_call(receiver_nick)
    chat_id = chat_checker(user_id_send, user_id_recv, chat_id=True)

    if isinstance(chat_id, np.int64):
        conn = engine_connector()

        query = f"""INSERT INTO chat_api.chat_messages (chat_id, user_id, message, message_date)
        VALUES ('{chat_id}', '{user_id_send}', '{string_fixer(message, to_db=True)}', '{datetime.now()}');
        """
        conn.execute(query)

        return "Message succesfully sent"
    else:
        return chat_id

@app.route('/chat/list')
def get_chat():
    user_id = user_call(request.args.get('user_nick'))
    recv_id = user_call(request.args.get('recv_nick'))
    chat_id = chat_checker(user_id, recv_id, chat_id=True)

    try:
        conn = engine_connector()

        query = f"""SELECT 
                        chat_id, 
                        chat_api.chat_messages.user_id AS user_id, 
                        chat_api.users.user_nick AS user_nick, 
                        message, 
                        message_date 
                    FROM chat_api.chat_messages
                    JOIN chat_api.users ON 
                        chat_api.chat_messages.user_id = chat_api.users.user_id
                    WHERE chat_id = {chat_id}
                """
        res = pd.read_sql(con=conn, sql=query).to_json(date_format='iso', force_ascii=True)
        return json.loads(res)
    except:
        return chat_id
        
## GROUPS ##

@app.route('/group/create')
def new_group():
    args = request.args
    res = {k: v for k, v in args.items()}
    
    if 'admin_nick' in res and 'group_name' in res:
        q_columns = ['group_name', 'user_id_admin', 'user_1_id', 'user_2_id', 'user_3_id']
        q_len = len(res)

        q_columns_str = ', '.join(q_columns[:q_len])

        group_name = res.pop('group_name')
        users_ids = [user_call(x) for x in res.values()]
        comillas = lambda x: "'"+str(x)+"'"
        comillado = list(map(comillas, users_ids))
        q_values_str = ', '.join(comillado)

        conn = engine_connector()

        query = f"""INSERT INTO chat_api.users_has_groups ({q_columns_str})
                        VALUES ('{group_name}', {q_values_str});
                    """
        conn.execute(query)

    return f"Group {group_name} succesfully created"    

@app.route('/group/addmessage')
def group_add_message():
    group_name = request.args.get('group_name')
    sender_nick = request.args.get('sender_nick')
    message = request.args.get('message')

    sender_id = user_call(sender_nick)
    group_id = group_checker(group_name, sender_id)

    if isinstance(group_id, np.int64):
        conn = engine_connector()

        query = f"""INSERT INTO chat_api.group_messages (group_id, user_id, group_name, message, message_date)
        VALUES ('{group_id}', '{sender_id}', '{group_name}', '{string_fixer(message, to_db=True)}', '{datetime.now()}');
        """
        conn.execute(query)

        return "Message succesfully sent"
    else:
        return group_id

@app.route('/group/adduser')
def group_add_user():
    group_name = request.args.get('group_name')
    new_user = request.args.get('new_user_nick')

    admin_id = user_call(request.args.get('admin_nick'))
    new_user_id = user_call(new_user)
    group_id = group_checker(group_name, admin_id, new_user=new_user, check_admin=True, check_space=True)

    if isinstance(group_id, tuple):
        group_id, column = group_id[0], group_id[1]
        conn = engine_connector()

        query = f"""UPDATE chat_api.users_has_groups 
                    SET {column} = {new_user_id}
                    WHERE group_id = {group_id};
                """

        conn.execute(query)

        return f"User '{new_user}' succesfully added to group '{group_name}'"
    else:
        return group_id

@app.route('/group/list')
def get_group():
    group_name = request.args.get('group_name')
    user_id = user_call(request.args.get('user_nick'))

    group_id = group_checker(group_name, user_id)

    try:
        conn = engine_connector()

        query = f"""SELECT 
                        group_id, 
                        chat_api.group_messages.user_id AS user_id, 
                        chat_api.users.user_nick AS user_nick, 
                        message, 
                        message_date 
                    FROM chat_api.group_messages
                    JOIN chat_api.users ON 
                        chat_api.group_messages.user_id = chat_api.users.user_id
                    WHERE group_id = {group_id}
                """
        res = pd.read_sql(con=conn, sql=query).to_json(date_format='iso', force_ascii=True)
        return json.loads(res)
    except:
        return group_id

