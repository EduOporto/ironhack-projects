from app import app
from flask import request
from bson import json_util
from sql_caller import engine_connector, user_call

## Endpoints

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

@app.route('/chat/create')
def new_chat():
    sender_nick = request.args.get('sender_nick') 
    receiver_nick = request.args.get('recv_nick')
    
    user_id_send = user_call(sender_nick)
    user_id_recv = user_call(receiver_nick)

    conn = engine_connector()

    query = f"""INSERT INTO chat_api.users_has_chats (chat_name, user_id_send, users_id_recv)
    VALUES ('{sender_nick}-{receiver_nick}', '{user_id_send}', '{user_id_recv}');
    """
    conn.execute(query)

    return f"Chat between {sender_nick} and {receiver_nick} succesfully added to our databases"

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