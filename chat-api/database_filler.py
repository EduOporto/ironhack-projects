# Fill Databases with random data

import requests
import api.chat_api_libs.sql_caller as sql 
from randomuser import RandomUser
from itertools import combinations
from random import choice, shuffle, sample
from random_words import RandomWords
from api.quotes.get_quotes import get_quotes
from api.chat_api_libs.string_fixer import string_fixer
import json

### SQL Database connection

conn = sql.engine_connector()

### Add 40 users to database

user_list = RandomUser.generate_users(40)

for user in user_list:
    users_dict = {'name':user.get_first_name(), 'last_name':user.get_last_name(), 'nick_name':user.get_username()}
    endpoint = "new_user?user_name={name}&user_surname={last_name}&user_nick={nick_name}".format(**users_dict)
    
    requests.get("http://127.0.0.1:5000/" + endpoint)

### Generate random chats

users_list = sql.get_users()['user_nick'].tolist()

selection = sample(users_list, 10)
chats_comb = list(combinations(selection, 2))
ten_chats = sample(chats_comb, 10)

for chat in ten_chats:
    chat_dict = {'sender_nick': chat[0], 'recv_nick': chat[1]}
    endpoint = "chat/create?sender_nick={sender_nick}&recv_nick={recv_nick}".format(**chat_dict)
    
    requests.get("http://127.0.0.1:5000/" + endpoint)

### Generate random groups

rw = RandomWords()

users_list = sql.get_users()['user_nick'].tolist()

for _ in range(10):
    n_users = choice(range(1,5))
    users = sample(users_list, n_users)
    args = ['&admin_nick=', '&recv1_nick=', '&recv2_nick=', '&recv3_nick=']
    group_name = rw.random_word()

    users_str = ''.join([e[0]+e[1] for e in list(zip(args, users))])

    endpoint = f"group/create?group_name={group_name}&" + users_str

    requests.get("http://127.0.0.1:5000/" + endpoint)

### Add random messages to chats and groups

## Add conversations to chats

quotes_iter = get_quotes()
rand_chat = sql.get_chats(random_chat=True).split('-')
for _ in range(20):
    shuffle(rand_chat)
    sender_nick = rand_chat[0]
    recv_nick = rand_chat[1]
    message = string_fixer(next(quotes_iter))
    
    endpoint = f"chat/addmessage?sender_nick={sender_nick}&recv_nick={recv_nick}&message={message}"
    requests.get("http://127.0.0.1:5000/" + endpoint)

## Add conversations to groups

quotes_iter = get_quotes()

rand_group = sql.get_groups(random_group=True)
group_users = rand_group.iloc[:,2:].applymap(lambda x: sql.user_call(x, id=True)).values.tolist()[0]
group_users_filt = [user for user in group_users if 'nan' not in user]

group_name = rand_group['group_name'].to_list()[0]

for _ in range(20):
    sender_nick = choice(group_users_filt)
    message = string_fixer(next(quotes_iter))
    
    endpoint = f"group/addmessage?group_name={group_name}&sender_nick={sender_nick}&message={message}"
    requests.get("http://127.0.0.1:5000/" + endpoint)