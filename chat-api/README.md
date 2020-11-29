#### Add user
new_user?user_name=Angel&user_surname=Correa&user_nick=Correa

                            #### CHATS ####

#### Create chat
chat/create?sender_nick=Correa&recv_nick=Pelayo

#### Send message to chat
chat/addmessage?sender_nick=angrybird736&recv_nick=silvergoose367&message=Hello_its_me

#### Get chat history
chat/list?user_nick=Koke&recv_nick=Correa

                            #### GROUPS ####

#### Create group
group/create?group_name=Atleti&admin_nick=Pelayo&recv1_nick=Arda&recv2_nick=Koke

#### Send message to group
group/addmessage?group_name=Atleti&sender_nick=Koke&message=Hi_guys

#### Add user to group
group/adduser?group_name=Atleti&admin_nick=Pelayo&new_user_nick=Arda

#### Get group history
group/list?group_name=Atleti&user_nick=Pelayo
