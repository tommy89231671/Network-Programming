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
import stomp

conn=stomp.Connection10()

#import secrets

#f=open('/home/ubuntu/addr.txt','r')
host="0.0.0.0"
port=int()
activemq_host=''
if len(sys.argv) == 4:
    host=sys.argv[1]
    port=int(sys.argv[2])
    activemq_host=sys.argv[3]


mysql_host="npdbinstance.clvibnzutilv.us-east-1.rds.amazonaws.com"
activemq_port=61613
mysql_db = MySQLDatabase('np', user='tommy', password='123456789',host=mysql_host, port=3306)
#mysql_db.connect()







serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((host, port))

serversocket.listen(5)

instance_dict=dict()


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
        status=0
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
            user=command[space1+1:]
            status=0
        #status=1
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
        #status=1
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
class Club(Model):
    club = CharField(default='')
    member= CharField(default='')
    class Meta:
        database = mysql_db
class SampleListener(object):
    def on_message(self, headers, message):
        #print ('headers: %s' % headers)
        print ('message: %s' % message)
while True:

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    (clientsocket, address) = serversocket.accept()
    #print(clientsocket,address)
    command=clientsocket.recv(1024).decode()
    #cmd=command[:command.find(" ")]
    tmp=command.split()
    cmd=tmp[0]
    #print(cmd)
    print(command)
    server_json=""
    
    if cmd=="invite":
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
                try:
                    Invite.insert(user_me=row1["account"],user_invite=invite_to).execute()
                    #print("invite success")
                    msg="Success!"
                    msg_status=0
                except:
                    msg="Usage: invite <user> <id> "
                    msg_status=1
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
                try:
                    msg=invitation+" did not invite you"
                    msg_status=1
                except:
                    msg="Usage: accept-invite <user> <id>"
                    msg_status=1  
            else:
                try:
                    Friend.insert(me=row1["account"],friend=invitation).execute()
                    Friend.insert(me=invitation,friend=row1["account"]).execute()
                    Invite.delete().where(Invite.user_me==invitation,Invite.user_invite==row1["account"]).execute()
                    msg="Success!"
                    msg_status=0
                except:
                    msg="Usage: accept-invite <user> <id>"
                    msg_status=1
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
            #status=1

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
                try:
                    Post.insert(user=row1["account"],post=content).execute()
                    server_json=json.dumps({ 'status': 0,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))
                except:
                    server_json=json.dumps({ 'status': 1,'message': "Usage: post <user> <message>"}, sort_keys=True, indent=4, separators=(',', ': '))
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
    elif cmd=="send":
        space1=command.find(" ")
        space2=command.find(" ",space1+1)
        space3=command.find(" ",space2+1)
        status=0
        msg_status=0
        user=None
        friend=None
        content=None
        if space2!=-1:
            user=command[space1+1:space2]

            try:
                if space3!=-1:
                    friend=command[space2+1:space3]
                    content=command[space3+1:]
                else:
                    status=0
            except:
                status=0
        else:
            #user=command[space1+1:]
            status=0
        if status==0:
            print(user,friend,content)
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            row2=dict()
            query2=User.select(User.account,User.password,User.token).where(User.account==friend).dicts()
            row3=dict()

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
                query3=Friend.select().where(Friend.me==row1["account"],Friend.friend==friend).dicts()
                row3=query3[0]
            except:
                row3=dict()

            if len(row1)==0:
                """login or not"""
                #print("not login yet")
                msg="Not login yet"
                msg_status=1
            elif len(row2)==0:
                """No such friend_id"""
                #print("id doesn't exit")
                if space3==-1:
                    msg="Usage: send <user> <friend> <message>"
                    msg_status=1
                else:
                    msg="No such user exist"
                    msg_status=1
            elif len(row3)==0:
                """Not friend relationship"""
                msg=friend+" is not your friend"
                msg_status=1
            elif row2["token"]=="":
                """Not online"""
                msg=friend+" is not online"
                msg_status=1
            else:
                """Success"""
                conn = stomp.Connection10([(activemq_host,activemq_port)])
                conn.start()
                conn.connect()
                queue_name="/queue/"+friend
                #<<<USER_A->USER_B: HELLO WORLD>>>
                sending_msg="<<<"+row1["account"]+"->"+friend+" :"+content+">>>"

                conn.send(queue_name,sending_msg)
                conn.disconnect()
                server_json=json.dumps({ 'status': 0,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))
            if msg_status==1:
                server_json=json.dumps({ 'status': 1,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))

        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: send <user> <friend> <message>"}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="create-group":
        status,me,group=two_parameter(command)
        print(me,group)
        msg=""
        msg_status=0
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==me).dicts()

            row2=list()
            query2=Club.select(Club.club,Club.member).where(Club.club==group).dicts()

            try:
                row1=query1[0]
            except:
                row1=dict()

            try:
                for i in query2:
                    row2.append(i)
            except:
                row2=list()
            #print(row2)
            if len(row1)==0:
                """login or not"""
                print("not login yet")
                msg="Not login yet"
                msg_status=1
                
            elif len(row2)!=0:

                """find invite id"""
                #print("id doesn't exit")
                msg=group+" already exist"
                msg_status=1
            else:
                try:
                    Club.insert(club=group,member=row1["account"]).execute()
                    msg="Success!"
                    msg_status=0
                except:
                    msg="Usage: create-group <user> <group>"
                    msg_status=1
        else:
            #print("usage wrong")
            msg="Usage: create-group <user> <group>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="list-group":
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
                query2=Club.select(Club.club).distinct().dicts()
                group_list=list()

                for row in query2:
                    group_list.append(row["club"])

                msg_group=group_list
                server_json=json.dumps({ 'status': 0,'friend': msg_group}, sort_keys=True, indent=4)
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: list-group <user>"}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="list-joined":
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
                query2=Club.select(Club.club,Club.member).where(Club.member==row1["account"]).dicts()
                group_list=list()

                for row in query2:
                    group_list.append(row["club"])

                msg_group=group_list
                server_json=json.dumps({ 'status': 0,'friend': msg_group}, sort_keys=True, indent=4)
        else:
            server_json=json.dumps({ 'status': 1,'message': "Usage: list-joined <user>"}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="join-group":
        status,me,group=two_parameter(command)
        msg=""
        msg_status=0
        if status==0:
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==me).dicts()

            row2=list()
            query2=Club.select(Club.club,Club.member).where(Club.club==group).dicts()

            try:
                row1=query1[0]
            except:
                row1=dict()

            try:
                for i in query2:
                    row2.append(i)
            except:
                row2=list()

            row3=dict()
            try:
                query3=Club.select(Club.club,Club.member).where(Club.club==group,Club.member==row1["account"]).dicts()
                row3=query3[0]
            except:
                row3=dict()
            #print(row2)
            if len(row1)==0:
                """login or not"""
                #print("not login yet")
                msg="Not login yet"
                msg_status=1
            elif len(row2)==0:

                """find invite id"""
                #print("id doesn't exit")
                msg=group+" does not exist"
                msg_status=1
            elif len(row3)!=0:
                msg="Already a member of "+group
                msg_status=1
            else:
                try:
                    Club.insert(club=group,member=row1["account"]).execute()
                    msg="Success!"
                    msg_status=0
                except:
                    msg="Usage: join-group <user> <group>"
                    msg_status=1
        else:
            #print("usage wrong")
            msg="Usage: join-group <user> <group>"
            msg_status=1
        server_json=json.dumps({ 'status': msg_status,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
    elif cmd=="require_subscribe_list":
        space=command.find(" ")
        user=command[space+1:]

        row1=list()
        query1=Club.select(Club.club,Club.member).where(Club.member==user).dicts()
        try:
            for i in query1:
                row1.append(i["club"])
        except:
            row1=list()
        server_json=json.dumps({ 'status': 0,'list': row1}, sort_keys=True, indent=4)


    elif cmd=="send-group":
        space1=command.find(" ")
        space2=command.find(" ",space1+1)
        space3=command.find(" ",space2+1)
        status=0
        msg_status=0
        user=None
        group=None
        content=None
        if space2!=-1:
            user=command[space1+1:space2]

            try:
                if space3!=-1:
                    group=command[space2+1:space3]
                    content=command[space3+1:]
                else:
                    status=0
            except:
                status=0
        else:
            #user=command[space1+1:]
            status=0
        suc=0
        if status==0:
            #print(user,group,content)
            row1=dict()
            query1=User.select(User.account,User.password,User.token).where(User.token==user).dicts()
            row2=dict()
            query2=Club.select().where(Club.club==group).dicts()
            row3=dict()

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
                query3=Club.select().where(Club.club==group,Club.member==row1["account"]).dicts()
                row3=query3[0]
            except:
                row3=dict()

            if len(row1)==0:
                """login or not"""
                #print("not login yet")
                msg="Not login yet"
                msg_status=1
            elif len(row2)==0:
                """No such group"""
                #print("id doesn't exit")
                if content!=None:
                    
                    msg="No such group exist"
                    msg_status=1
                else:
                    msg="Usage: send-group <user> <group> <message>"
                    msg_stauss=1
            elif len(row3)==0:
                """Not friend relationship"""
                msg="You are not the member of "+group
                msg_status=1

            else:
                """Success"""
                suc=1
                conn = stomp.Connection10([(activemq_host,activemq_port)])
                conn.start()
                conn.connect()
                topic_name="/topic/"+group
                #<<<USER_A->USER_B: HELLO WORLD>>>
                sending_msg="<<<"+row1["account"]+"->GROUP<"+group+">:"+content+">>>"
                
                conn.send(topic_name,sending_msg)
                conn.disconnect()
                server_json=json.dumps({ 'status': 0,'message': "Success!"}, sort_keys=True, indent=4, separators=(',', ': '))
            #print(msg,msg_status)
            if msg_status==1:
                server_json=json.dumps({ 'status': 1,'message': msg}, sort_keys=True, indent=4, separators=(',', ': '))
                
            elif suc!=1:
                server_json=json.dumps({ 'status': 1,'message': "Usage: send-group <user> <group> <message>"}, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        server_json=json.dumps({ 'status': 1,'message': "Unknown command "+cmd}, sort_keys=True, indent=4, separators=(',', ': '))
    

    clientsocket.send(server_json.encode())
    #time.sleep(1)

    """
    login gakki 123
    login satomi 123
    send gakki satomi wewewewe

    """
