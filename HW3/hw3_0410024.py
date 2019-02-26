# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:49:28 2018

@author: tommy
"""
#import  pymysql 

import os
from peewee import *
from peewee import CharField
from peewee import MySQLDatabase
from peewee import Model
from playhouse.db_url import connect
import socket
import uuid
import json
import sys
#import secrets

mysql_db = MySQLDatabase('NP', user='tommy', password='123',host='140.113.67.107', port=3306)
#mysql_db.connect()
host=""
port=int()
if len(sys.argv) == 3:
    host=sys.argv[1]
    port=int(sys.argv[2])
#host = '10.0.2.15'
#port = 374

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((host, port))

serversocket.listen(5)



def two_parameter(command):
    space1=command.find(" ")
    space2=command.find(" ",space1+1)
    
    if(space2!=-1):    
        space3=command.find(" ",space2+1)
            
    user=None
    password=None
    status=0
    if space1==-1:
        #print("wrong")
        status=1
    elif space2!=-1:
        if space3!=-1:
            status=1
        else:
            user=command[space1+1:space2]
            password=command[space2+1:]
    elif space2==-1:
        user=None
        password=None
        if command[:space1]=="register" or command[:space1]=="login":
            status=1
        else:
            status=0
   # else:
        
        #msg=logout(user,trash)
        
    return status,user,password

def one_parameter(command):
    space1=command.find(" ")
    space2=command.find(" ",space1+1)
    status=0
    user=None
    if space2!=-1:
        status=1
    elif space1==-1:
        user=None
        #print("in")
    else:
        #print("in")
        user=command[space1+1:]
    return status,user
class User(Model):
    account = CharField(default='')
    password = CharField(default='')
    token= CharField(default='')
    class Meta:
        database = mysql_db
class Invite(Model):
    user_me = CharField(default='')
    user_invite= CharField(default='')
    class Meta:
        database = mysql_db
class Friend(Model):
    me = CharField(default='')
    friend= CharField(default='')
    class Meta:
        database = mysql_db
class Post(Model):
    user = CharField(default='')
    post= CharField(default='')
    class Meta:
        database = mysql_db
while True:
    
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    (clientsocket, address) = serversocket.accept()
    #print(clientsocket,address)
    command=clientsocket.recv(1024).decode()
    #cmd=command[:command.find(" ")]  
    tmp=command.split()
    cmd=tmp[0]
    print(command)
    server_json=""
    if cmd=="register":
        status,user,pw=two_parameter(command)
        msg=""
        msg_status=0
        if status==0:
            try:
                User.insert(account=user,password=pw).execute()
                #print("success")
                msg="Success!"
                msg_status=0
            except:
                #print("id has been used")
                msg=user+" is already used"
                msg_status=1
        else:
            #print("usage wrong")
            msg="Usage: register <id> <password>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="login":
        status,user,pw=two_parameter(command)
        if status==0:
            row=dict()
            token=""
            a=User.select(User.account,User.password,User.token).where(User.account==user,User.password==pw).dicts()
#            for row in a:
#                print(row)
            try:
                row=a[0]
            except:
                row=dict()
            #print(len(row))
            if len(row)==0:
                #print("id or password wrong")
                server_json=json.dumps({ 'status': 1,'message': "No such user or password error"}, sort_keys=True, indent=4, separators=(',', ': '))
            elif row["token"]=="":
                token=uuid.uuid4().hex
                User.update(**{"token": token}).where(User.account==user,User.password==pw).execute()
                #print("success")
                server_json=json.dumps({ 'status': 0,'token':token ,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))

            elif row["token"]!="":
                token=row["token"]
                #print("success")
                server_json=json.dumps({ 'status': 0,'token':token ,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))

        else:
            #print("usage wrong")
            server_json=json.dumps({ 'status': 1,'message': "Usage: login <id> <password>"}, sort_keys=True, indent=4, separators=(',', ': '))
            
    elif cmd=="logout":
        status,token=one_parameter(command)
        msg=""
        msg_status=0
        if status==0:
            row=dict()
            a=User.select(User.account,User.password,User.token).where(User.token==token).dicts()
            try:
                row=a[0]
            except:
                row=dict()
            if len(row)==0:
                
                #print("not login yet")
                #server_json=json.dumps({ 'status': 1,'message': "Usage: login <id> <password>"}, sort_keys=True, indent=4, separators=(',', ': '))
                msg="Not login yet"
                msg_status=1
            else:
                User.update(**{"token": ""}).where(User.account==row["account"]).execute()
                #print("Bye")
                msg="Bye!"
                msg_status=0
        else:
            msg="Usage: logout <user>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="delete":
        status,token=one_parameter(command)
        if status==0:
            row=dict()
            a=User.select(User.account,User.password,User.token).where(User.token==token).dicts()
            try:
                row=a[0]
            except:
                row=dict()
            if len(row)==0:
                #print("not login yet")
                msg="Not login yet"
                msg_status=1
            else:
                
                Invite.delete().where((Invite.user_me==row["account"])|(Invite.user_invite==row["account"])).execute()
                Friend.delete().where((Friend.me==row["account"])|(Friend.friend==row["account"])).execute()
                Post.delete().where(Post.user==row["account"]).execute()
                User.delete().where(User.account==row["account"]).execute()
                #print("Bye")
                msg="Success!"
                msg_status=0
        else:
            #print("usage wrong")
            msg="Usage: delete <user>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="invite":
        status,me,invite_to=two_parameter(command)
        msg=""
        msg_status=0
        if status==0:
            
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==me).dicts()
            
            row2=dict()
            query2=User.select(User.account,User.password,User.token).where(User.account==invite_to).dicts()
            row3=dict()
            row4=dict()
            row5=dict()
            try:
                row1=query1[0]
            except:
                row1=dict()
            
            try:
                row2=query2[0]
            except:
                row2=dict()
            try:
                row3=dict()
                query3=Invite.select().where(Invite.user_me==row1["account"],Invite.user_invite==invite_to).dicts()
                row3=query3[0]
            except:
                row3=dict()
            try:
                row4=dict()
                query4=Invite.select().where(Invite.user_me==invite_to,Invite.user_invite==row1["account"]).dicts()
                row4=query4[0]
            except:
                row4=dict()
            try:
                row5=dict()
                query5=Friend.select().where(Friend.me==row1["account"],Friend.friend==invite_to).dicts()
                row5=query5[0]
            except:
                row5=dict()
                
                
            if len(row1)==0:
                """login or not"""
                #print("not login yet")
                msg="Not login yet"
                msg_status=1
            elif len(row2)==0:
                """find invite id"""
                #print("id doesn't exit")
                msg=invite_to+" does not exist"
                msg_status=1
            elif row1["account"]==row2["account"]:
                """invite yourself"""
                #print("you can't invite yourself")
                msg="You cannot invite yourself"
                msg_status=1
            elif len(row3)!=0:
                #print("Already invited")
                msg="Already invited"
                msg_status=1
            elif len(row4)!=0:
                #print("<id> has invited you")
                msg=invite_to+" has invited you"
                msg_status=1
            elif len(row5)!=0:
                msg=invite_to+" is already your friend"
                msg_status=1
            else:
                Invite.insert(user_me=row1["account"],user_invite=invite_to).execute()
                #print("invite success")
                msg="Success!"
                msg_status=0
        else:
            #print("usage wrong")
            msg="Usage: invite <user> <id> "
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="list-invite":
        status,user=one_parameter(command)
        #print(user)
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            try:
                row1=query1[0]
            except:
                row1=dict()
            if len(row1)==0:
                server_json=json.dumps({ 'status': 1,'message': "Not login yet"}, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                #print("yes")
                query2=Invite.select().where(Invite.user_invite==row1["account"]).dicts()
                invitation=list()
                
                for row in query2:
                    invitation.append(row["user_me"])
                
                msg_invitation=invitation
                server_json=json.dumps({ 'status': 0,'invite': msg_invitation}, sort_keys=True, indent=4)
                #print(server_json)
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: list-invite <user>"}, sort_keys=True, indent=4, separators=(',', ': '))
                
        #if status==0:
    elif cmd=="accept-invite":
        status,me,invitation=two_parameter(command)
        msg=""
        msg_status=0
        if status==0:
            
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==me).dicts()
            row2=dict()
            try:
                row1=query1[0]
                #print(row1["account"])
#                query2=Invite.select(Invite.user_me,Invite.user_invite).where(Invite.user_me==invitation,Invite.user_invite==row1["account"]).dicts()
#                row2=query2[0]
            except:
                row1=dict()
                
            try:
                query2=Invite.select(Invite.user_me,Invite.user_invite).where(Invite.user_me==invitation,Invite.user_invite==row1["account"]).dicts()
                row2=query2[0]
            except:
                row2=dict()
                
                
#            for row2 in query2:
#                print(row2)
            if len(row1)==0:
                msg="Not login yet"
                msg_status=1
            elif len(row1)!=0 and len(row2)==0:
                msg=invitation+" did not invite you"
                msg_status=1
            else:
                Friend.insert(me=row1["account"],friend=invitation).execute()
                Friend.insert(me=invitation,friend=row1["account"]).execute()
                Invite.delete().where(Invite.user_me==invitation,Invite.user_invite==row1["account"]).execute()
                msg="Success!"
                msg_status=0
        else:
            msg="Usage: accept-invite <user> <id>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
#    elif cmd=="exit":
#        mysql_db.close()
#        clientsocket.close()
#        serversocket.close()
#        #sys.exit(1)
#        break
    elif cmd=="list-friend":
        status,user=one_parameter(command)
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            try:
                row1=query1[0]
            except:
                row1=dict()
            if len(row1)==0:
                server_json=json.dumps({ 'status': 1,'message': "Not login yet"}, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                query2=Friend.select().where(Friend.me==row1["account"]).dicts()
                friend_list=list()
                    
                for row in query2:
                    friend_list.append(row["friend"])
                    
                msg_friend=friend_list
                server_json=json.dumps({ 'status': 0,'friend': msg_friend}, sort_keys=True, indent=4) 
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: list-friend <user>"}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="post":
        #status,user,content=two_parameter(command)
        space1=command.find(" ")
        space2=command.find(" ",space1+1)
        status=0
        user=None
        content=None
        if space2!=-1:
            user=command[space1+1:space2]
            try:
                content=command[space2+1:]
            except:
                status=1
        
        else:
            user=command[space1+1:]
            status=1
            
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            try:
                row1=query1[0]
            except:
                row1=dict()
            if len(row1)==0:
                server_json=json.dumps({ 'status': 1,'message': "Not login yet"}, sort_keys=True, indent=4, separators=(',', ': '))
            
            else:
                Post.insert(user=row1["account"],post=content).execute()
                server_json=json.dumps({ 'status': 0,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: post <user> <message>"}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="receive-post":
        status,user=one_parameter(command)
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            try:
                row1=query1[0]
            except:
                row1=dict()
            if len(row1)==0:
                server_json=json.dumps({ 'status': 1,'message': "Not login yet"}, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                query2=Friend.select(Friend.friend,Post.post).join(Post,on=(Friend.friend==Post.user)).where(Friend.me==row1["account"]).dicts()
#                for row in query2:
#                    print(row)
                
                
                post_list=list()
                for row in query2:
                    row['id'] = row.pop('friend')
                    row['message'] = row.pop('post')
                    post_list.append(row)
                    #friend_list.append(row["friend"])
                #print(post_list)
                #print(friend_list)
                msg_post_list=post_list
                server_json=json.dumps({ 'status': 0,'post': msg_post_list}, sort_keys=True, indent=4) 
                #print(server_json)
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: receive-post <user>"}, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        server_json=json.dumps({ 'status': 1,'message': "Unknown command "+cmd}, sort_keys=True, indent=4, separators=(',', ': '))
        
    
    clientsocket.send(server_json.encode())
#    res = (User.insert(account="0410024",password="0410024",token=secrets.token_hex(16)).execute())
#    query = User.select()
#    for a in query:
#        print(a.account)