# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:34:48 2018

@author: tommy
"""

import socket
import json
import sys
import stomp
import threading
import random
import time
HOST = ""
PORT = ""
activemq_host="192.168.0.104"
activemq_port=61613
login_dict=dict()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
subscribe_dict=dict()
def direct(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
def two_parameter(command):
    space1=command.find(" ")
    space2=command.find(" ",space1+1)
    user=None
    trash=None

    if(space2==-1):
        user=command[space1+1:]
        #msg=logout(user,None)
    else:
        user=command[space1+1:space2]
        trash=command[space2+1:]
        #msg=logout(user,trash)

    return user,trash
def three_parameter(command):
    space1=command.find(" ")
    space2=command.find(" ",space1+1)
    if(space2!=-1):
        space3=command.find(" ",space2+1)

    user=None
    friend=None
    trash=None
    if(space2==-1):
        user=command[space1+1:]
    elif(space2!=-1 and space3==-1):
        user=command[space1+1:space2]
        friend=command[space2+1:]
    elif(space2!=-1 and space3!=-1):
        user=command[space1+1:space2]
        friend=command[space2+1:space3]
        trash=command[space3+1:]
    return user,friend,trash
def four_parameter(command):
    space1=command.find(" ")
    space2=command.find(" ",space1+1)
    space3=command.find(" ",space2+1)
    user=None
    friend=None
    msg=None
    if space2==-1:
        user=command[space1+1:]
    elif (space2!=-1 and space3==-1):
        user=command[space1+1:space2]
        friend=command[space2+1:]
    else:
        user=command[space1+1:space2]
        friend=command[space2+1:space3]
        msg=command[space3+1:]
    return user,friend,msg


def register(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    #print(s.recv(1024))
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]

def login(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    #return text["status"],text["message"],text["token"]
    if(text["status"]==0):
        return text["status"],text["message"],text["token"]
    else:
        return text["status"],text["message"],None
def logout(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):

        cmd="logout "+token+" "+trash
    else:
        cmd="logout "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        del login_dict[user]

    #print(login_dict)
    return text["message"]
def delete(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):
        cmd="delete "+token+" "+trash
    else:
        cmd="delete "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        del login_dict[user]
    #print(login_dict)
    return text["message"]
def invite(user,friend,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(friend==None):
        cmd="invite "+token
    elif(friend!=None and trash==None):
        cmd="invite "+token+" "+friend
    else:
        cmd="invite "+token+" "+friend+" "+trash
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    #print(login_dict)
    return text["message"]
def list_invite(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):
        cmd="list-invite "+token+" "+trash
    else:
        cmd="list-invite "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["invite"]
    else:
        return text["status"],text["message"]
    #print(login_dict)
    #return text["message"]
def accept_invite(user,friend,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(friend==None):
        cmd="accept-invite "+token
    elif(friend!=None and trash==None):
        cmd="accept-invite "+token+" "+friend
    else:
        cmd="accept-invite "+token+" "+friend+" "+trash
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"]
def list_friend(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):
        cmd="list-friend "+token+" "+trash
    else:
        cmd="list-friend "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def post(user,content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(content!=None):
        cmd="post "+token+" "+content
    else:
        cmd="post "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
def receive_post(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):
        cmd="receive-post "+token+" "+trash
    else:
        cmd="receive-post "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["post"]
    else:
        return text["status"],text["message"]
def send(user,friend,msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    cmd=""
    try:
        token=login_dict[user]
    except:
        token=user
    if friend!=None:
        if msg!=None:
            cmd="send "+token+" "+friend+" "+msg
        else:
            cmd="send "+token+" "+friend
    else:
        if msg!=None:
            cmd="send "+token+" "+msg
        else:
            cmd="send"
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
class SampleListener(object):
    def on_message(self, headers, message):
        #print ('headers: %s' % headers)
        print (message)
conn_dict=dict()
def receive_from_queue(conn,listener_name):
    #while 1:

        conn.set_listener(listener_name, SampleListener())
        conn.start()
        conn.connect()
        queue_name="/queue/"+listener_name
        conn.subscribe(destination=queue_name,id=random.randint(1,100))

        #conn.subscribe()
        #time.sleep(1) # secs
        #conn_list.append((conn,listener_name))

        conn_dict[listener_name].append((conn,queue_name))
        time.sleep(0.11)
        #print(conn)
        #conn.disconnect()
def receive_from_topic(user,group):
        #conn = stomp.Connection10([(activemq_host,activemq_port)])
        conn.set_listener(user, SampleListener())
        conn.start()
        conn.connect()
        topic_name='/topic/'+group
        try:
            conn.subscribe(destination=topic_name,id=random.randint(1,100))
            conn_dict[user].append((conn,topic_name))
            time.sleep(0.1)
        except:
            receive_from_topic(user,group)
        #conn.disconnect()
def get_group_list(user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    cmd="require_subscribe_list "+user
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["status"],text["list"]
def unsubscribe(listener_name):
    #print(conn_dict[listener_name])
    for conn in conn_dict[listener_name]:
        #print(conn)
        #print(conn[0],conn[1])
        #conn[0].start()
        conn[0].connect()
        #queue_name="/queue/"+listener_name

        #conn.unsubscribe(destination=queue_name,id=12)
        conn[0].unsubscribe(destination=conn[1])
        #time.sleep(1) # secs
        conn[0].disconnect()
def create_group(user,group,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    token=""
    try:
        token=login_dict[user]
    except:
        token=user
    if(group==None):
        cmd="create-group "+token
    elif(group!=None and trash==None):
        cmd="create-group "+token+" "+group
    else:
        cmd="create-group "+token+" "+group+" "+trash
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"],text["status"]
def list_group(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    token=""
    try:
        token=login_dict[user]
    except:
        token=user
    if(trash!=None):
        cmd="list-group "+token+" "+trash
    else:
        cmd="list-group "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def list_joined(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    token=""
    try:
        token=login_dict[user]
        #print(token)
    except:
        token=user
    if(trash!=None):
        cmd="list-joined "+token+" "+trash
    else:
        cmd="list-joined "+token
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def join_group(user,group,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    token=""
    try:
        token=login_dict[user]
    except:
        token=user
    if(group==None):
        cmd="join-group "+token
    elif(group!=None and trash==None):
        cmd="join-group "+token+" "+group
    else:
        cmd="join-group "+token+" "+group+" "+trash
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"],text["status"]
def send_group(user,group,msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    cmd=""
    try:
        token=login_dict[user]
        #print(token)
    except:
        token=user
    if group!=None:
        if msg!=None:
            cmd="send-group "+token+" "+group+" "+msg
        else:
            cmd="send-group "+token+" "+group
    else:
        if msg!=None:
            cmd="send-group "+token+" "+msg
        else:
            cmd="send-group"
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
if __name__ == '__main__':

    #command=input("cmd:")
    subscribe_id_counter=0
    host=""
    port=int()
    if len(sys.argv) == 3:
        HOST=sys.argv[1]
        PORT=int(sys.argv[2])
    thread_list=list()
    #HOST=input("IP:")
    #PORT=int(input("Port:"))

    while(1):
    #command="login 0410024 0410024"


        command=input()
        cmd=command[:command.find(" ")]

        if(cmd=="register"):
            msg=register(command)
            print(msg)

        elif(cmd=="login"):
            tmp=command.find(" ")
            user=command[tmp+1:command.find(" ",tmp+1)]
            status,msg,token=login(command)
            if(status==0):
                login_dict.update({user:token})
            #print(status,msg,token)
            print(msg)

            if msg=="Success!":
                conn = stomp.Connection10([(activemq_host,activemq_port)])
                conn.set_listener(user, SampleListener())
                conn.start()
                conn.connect()

                conn_dict[user]=conn
                subscribe_dict.setdefault(user, [])
                topic_list=list()
                conn.subscribe(destination="/queue/"+user,id=subscribe_id_counter)
                subscribe_dict[user].append(subscribe_id_counter)
                subscribe_id_counter+=1
                #receive_from_queue(conn,user)
                text=get_group_list(user)
                topic_list=text[1]
                for a in topic_list:
                    conn.subscribe(destination="/topic/"+a,id=subscribe_id_counter)
                    subscribe_dict[user].append(subscribe_id_counter)
                    subscribe_id_counter+=1

        elif(cmd=="logout"):
            user,trash=two_parameter(command)
            msg=logout(user,trash)
            print(msg)
            if msg=="Bye!":
                subscribe_delete_list=subscribe_dict[user]
                connect_delete=conn_dict[user]
                for a in subscribe_delete_list:
                    connect_delete.unsubscribe(id=a)
                connect_delete.disconnect()
                del subscribe_dict[user]
                del conn_dict[user]
        elif(cmd=="delete"):
            user,trash=two_parameter(command)
            msg=delete(user,trash)
            print(msg)
            if msg=="Success!":
                subscribe_delete_list=subscribe_dict[user]
                connect_delete=conn_dict[user]
                for a in subscribe_delete_list:
                    connect_delete.unsubscribe(id=a)
                connect_delete.disconnect()
                del subscribe_dict[user]
                del conn_dict[user]
        elif(cmd=="invite"):
            user,friend,trash=three_parameter(command)
            msg=invite(user,friend,trash)
            print(msg)
        elif(cmd=="list-invite"):
            user,trash=two_parameter(command)
            status,msg=list_invite(user,trash)
            if(status==0):
                if len(msg)==0:
                    print("No invitations")
                else:
                    for i in msg:
                        print(i)
            else:
                print(msg)
        elif(cmd=="accept-invite"):
            user,friend,trash=three_parameter(command)
            msg=accept_invite(user,friend,trash)
            print(msg)
        elif(cmd=="list-friend"):
            user,trash=two_parameter(command)
            status,msg=list_friend(user,trash)
            if(status==0):
                if len(msg)==0:
                    print("No friends")
                else:
                    for i in msg:
                        print(i)
            else:
                print(msg)
        elif(cmd=="post"):
            user,content=two_parameter(command)
            msg=post(user,content)
            print(msg)
        elif(cmd=="receive-post"):
            user,trash=two_parameter(command)
            status,msg=receive_post(user,trash)
            if(status==0):
                if len(msg)==0:
                    print("No Posts")
                else:
                    for i in msg:
                        print(i["id"]+":"+i["message"])
            else:
                print(msg)
        elif cmd=="send":
            user,friend,content=four_parameter(command)
            #print(user,friend,content)
            msg=send(user,friend,content)
            print(msg)
        elif cmd=="create-group":
            ###
            user,group,trash=three_parameter(command)
            msg,status=create_group(user,group,trash)
            print(msg)
            if status==0:
                #print(user,group)
                conn=conn_dict[user]
                conn.subscribe(destination="/topic/"+group,id=subscribe_id_counter)
                subscribe_dict[user].append(subscribe_id_counter)
                subscribe_id_counter+=1
                #receive_from_topic(user,group)
                #<<<USER_A->USER_B: HELLO WORLD>>>
                #sending_msg="<<<"+row1["account"]+"->"+friend+" :"+content+">>>"

                #conn.send(topic_name,)
                #conn.subscribe(topic_name)
                #conn.disconnect()
        elif cmd=="list-group":
            user,trash=two_parameter(command)
            status,msg=list_group(user,trash)
            if(status==0):
                if len(msg)==0:
                    print("No groups")
                else:
                    for i in msg:
                        print(i)
            else:
                print(msg)
        elif cmd=="list-joined":
            user,trash=two_parameter(command)
            status,msg=list_joined(user,trash)
            if(status==0):
                if len(msg)==0:
                    print("No groups")
                else:
                    for i in msg:
                        print(i)
            else:
                print(msg)
        elif cmd=="join-group":
            ###
            user,group,trash=three_parameter(command)
            msg,status=join_group(user,group,trash)
            print(msg)
            if status==0:
                #print(user,group)
                conn=conn_dict[user]
                conn.subscribe(destination="/topic/"+group,id=subscribe_id_counter)
                subscribe_dict[user].append(subscribe_id_counter)
                subscribe_id_counter+=1
                #receive_from_topic(user,group)
        elif cmd=="send-group":
            ###
            user,group,content=four_parameter(command)
            #print(user,friend,content)
            msg=send_group(user,group,content)
            print(msg)
        else:
            if(command[0:4]=="exit"):
                #thread_list[0].delete()
                break
            else:
                print(direct(command))
        #print(conn_dict)
        #print(subscribe_dict)
