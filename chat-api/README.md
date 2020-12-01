# **CHAT API**

This repository comprises the creation, using flask, of an API that serves as backend for a chat service that besides allowing the registration of users, the communication among them or the creation of groups, also trys to analyze the feelings of those chats using NLTK sentiment analysis.

All data added to this API will be saved on a SQL database, in order to being able to acces it later, as user may request.

## **USAGE**
### **Creation of a new user**
In order to register a new user, you just need to enter the following endpoint, adding to it the parameters 'user_name', 'user_surname' and 'user_nick', which must be unique in the database. 

Example:

> new_user?user_name={...}&user_surname={...}&user_nick={...}
> 
> new_user?user_name=Jorge&user_surname=Resurreccion&user_nick=Koke

## **Chats**
### **Create a new chat**
This endpoint should get a 'sender_nick', which is the nickname of the user that is creating the chat; and a 'recv_nick', which is the nickname of the user that is receiving the chat. 

Example:

> chat/create?sender_nick={...}&recv_nick={...}
> 
> chat/create?sender_nick=Koke&recv_nick=Savic

### **Send a message to chat**
For this, the endpoint will need to get a 'sender_nick', which is the nick of the person who is sendin the message, a 'recv_nick', which is the nick of the person who is getting it, and a 'message', which words must be separated by underscores and must not contain special characters. 

Example:

> chat/addmessage?sender_nick={...}&recv_nick={...}&message={...}
>
> chat/addmessage?sender_nick=Koke&recv_nick=Savic&message=Aupa_Atleti

In order to make this operation easier I created the function *string_fixer*, which gets a string as a parameter and converts it to a format that is readable in the query.

~~~~
from chat_api_libs.string_fixer import string_fixer
    
string = "Today we play against Bayern Munich"
    
string_fixed = string_fixer(string)

# Must return: "Today_we_play_against_Bayern Munich" 
~~~~

### **Get chat history**
If the user wants to read the messages from a particular chat between him/her and another user, is as easy as insert the following endpoint, adding his/her nickname for 'user_nick and the nickname of the other user for 'recv_nick'. This will display a json file with all the messages sent to the conversation, the user that sent them and its date. 

Example:

> chat/list?user_nick={...}&recv_nick={...}
>
> chat/list?user_nick=Koke&recv_nick=Savic

### **Get chat history with sentiment analysis**
If the user wants to read the messages from a particular chat between him/her and another user, with the sentiment analysis attached to each of the messages, is as easy as insert the following endpoint, adding his/her nickname for 'user_nick and the nickname of the other user for 'recv_nick'. This will display a json file with all the messages sent to the conversation, the user that sent them and its date. 

Example:

> chat/list_mood?user_nick={...}&recv_nick={...}
>
> chat/list_mood?user_nick=Koke&recv_nick=Savic

## **Groups**

### **Create group**
In order to create a group, thre will always be one user who will be the administrator of it, the only able to add people to it. The limit of the groups will be four people (admin. included). This user must insert on the following endpoint the params 'group_name', which will be the name of the group, the 'admin_nick', which will be its nick, and the rest of the users' nicknames, which will be 'recv1_nick', 'recv2_nick' and 'recv3_nick' if needed.

IMPORTANT: An user can also create a group for him/her alone, in order to use it as notes or clipboard. 

Example:

> group/create?group_name={...}&admin_nick={...}&recv1_nick={...}&recv2_nick={...}
>
> group/create?group_name=Atleti&admin_nick=Koke&recv1_nick=Savic&recv2_nick=Correa

### **Add user to group**
The admin. of a group can add more users to it (if there is space left) using the following endpoint, writing on it the group name as 'group_name', his/her nickname as 'admin_nick', and the new user nickname as 'new_user_nick'.

Example:
> group/adduser?group_name={...}&admin_nick={...}&new_user_nick={...}
>
> group/adduser?group_name=Atleti&admin_nick=Pelayo&new_user_nick=Arda

### **Send message to group**
If an user wants to send a message to a group, it will be as easy as insert on the endpoint the name of the group as 'group_name', his/her nickname as 'sender_nick', and the message as 'message'. Here applies the same that for chat messages, and *string_fixer()* function can also be used. 

IMPORTANT: In order to send a message to a group, the user must be part of that group, otherwise the API call will be rejected.

Example:
> group/addmessage?group_name={...}&sender_nick={...}&message={...}
>
> group/addmessage?group_name=Atleti&sender_nick=Koke&message=Hi_guys

#### **Get group history**
If an user wants to read the messages sent to a particular group, he/she just need to use the following endpoint, adding to it the group name as 'group_name' and his/her nickname as 'user_nick'. This will display a json file with all the messages sent to the group, the user that sent them and its date.

IMPORTANT: In order to recover the messages from a group, the user must be part of that group, otherwise the API call will be rejected.

Example:
> group/list?group_name={...}&user_nick={...}
>
> group/list?group_name=Atleti&user_nick=Koke

#### **Get group history with sentiment analysis**
If an user wants to read the messages sent to a particular group, with the sentiment analysis attached to each of the messages, he/she just need to use the following endpoint, adding to it the group name as 'group_name' and his/her nickname as 'user_nick'. This will display a json file with all the messages sent to the group, the user that sent them and its date.

IMPORTANT: In order to recover the messages from a group, the user must be part of that group, otherwise the API call will be rejected.

Example:
> group/list_mood?group_name={...}&user_nick={...}
>
> group/list_mood?group_name=Atleti&user_nick=Koke


## **User history**
User will be able to recover a list of all the chats and groups he/she is in with a simple endpoint in which he/she must enter the nickname as 'user_nick'. This will display a json file with all the active chats and groups.

Example:
> user_hist?user_nick={...}
>
> user_hist?user_nick=Koke

## **SQL DATABASE DIAGRAMS**

In order to keep the original structure I created for this SQL database, I also attached to this repo the original [EER Diagrams](https://github.com/EduOporto/ironhack-projects/tree/main/chat-api/SQL_diagrams), so the user can import this very database easily. It will be enough to open the document ['chat_api_diagram.mwb'](https://github.com/EduOporto/ironhack-projects/blob/main/chat-api/SQL_diagrams/chat_api_diagram.mwb) and run the forward eingenieer in MySQL Workbench.

## **FEELINGS WITH DUMMIES**

In order to show how this API could analyze the feelings of a chat/group, I have created a python file that can fill the entire database, from adding random users to fill its chats and groups with random quotes. 

In order to see this, the whole python document called [database_filler.py](https://github.com/EduOporto/ironhack-projects/blob/main/chat-api/database_filler.ipynb) must be entirely ran.