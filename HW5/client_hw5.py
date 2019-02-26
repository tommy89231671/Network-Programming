# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 23:37:26 2019

@author: tommy
"""

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




login_HOST = ""
login_PORT = 0

app_HOST=""
app_PORT=0

#activemq_host="54.85.240.162"
activemq_port=61613
login_dict=dict()
app_conn_dict=dict()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
subscribe_dict=dict()
def direct(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    HOST=login_HOST
    PORT=login_PORT
    
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
    HOST=login_HOST
    PORT=login_PORT
    
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    #print(s.recv(1024))
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]

def login(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST=login_HOST
    PORT=login_PORT
    
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    try:
        text=json.loads(s.recv(1024).decode())
    except:
        text=json.loads(s.recv(1024).decode())
    s.close()
    
    #print(text)
    #return text["status"],text["message"],text["token"]
    if(text["status"]==0):
        return text["status"],text["message"],text["token"],text["app_conn_addr"],text['app_conn_port']
    else:
        return text["status"],text["message"],None,None,None
def logout(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST=login_HOST
    PORT=login_PORT
    s.connect((HOST, PORT))
    cmd=""
    try:
        token=login_dict[user]
    except:
        token=None
    if(trash!=None):
        if token==None:
            cmd="logout "+trash
        else:
            cmd="logout "+token+" "+trash
    else:
        if token!=None:
            cmd="logout "+token
        else:
            cmd="logout"
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        del login_dict[user]

    #print(login_dict)
    return text["message"]
def delete(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST=login_HOST
    PORT=login_PORT
    s.connect((HOST, PORT))
    cmd=""
    try:
        token=login_dict[user]
    except:
        token=None
    if(trash!=None):
        if token==None:
            cmd="delete "+trash
        else:
            cmd="delete "+token+" "+trash
    else:
        if token!=None:
            cmd="delete "+token
        else:
            cmd="delete"
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        try:
            del login_dict[user]
        except:
            aaa=None
            
    #print(login_dict)
    return text["message"]
def check_login(user):
    
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST=login_HOST
    PORT=login_PORT
    s.connect((HOST, PORT))
    cmd="Check_login "+user
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    #print(text)
    s.close()
    return text["status"]
    
    
def invite(user,friend,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #HOST=app_HOST
    #PORT=app_PORT
    #print(HOST,PORT)
#    
#    
#    s.connect((HOST, PORT))
#    #cmd=""
#    cmd="Check_login "+user
#    s.send(cmd.encode())
#    text=json.loads(s.recv(1024).decode())
#    print(text)
#    s.close()
#    
#    if text["status"]=="no":
#        return "Not login yet"
    #if check_login(user)=="no":
        #return "Not login yet"
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return "Not login yet"
    if(friend==None):
        if token!=None:
            cmd="invite "+token
        else:
            cmd="invite"
    elif(friend!=None and trash==None):
        if token!=None:
            cmd="invite "+token+" "+friend
        else:
            cmd="invite "+friend
    else:
        if token!=None:
            
            cmd="invite "+token+" "+friend+" "+trash
        else:
            cmd="invite "+friend+" "+trash
    #print(HOST,PORT)
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    #print(login_dict)
    return text["message"]
def list_invite(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #HOST=app_HOST
    #PORT=app_PORT
    #if check_login(user)=="no":
        #return 1,"Not login yet"
    
    
    
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return 1,"Not login yet"
    if(trash!=None):
        if token==None:
            cmd="list-invite "+trash
        else:
            cmd="list-invite "+token+" "+trash
    else:
        if token!=None:
            cmd="list-invite "+token
        else:
            cmd="list-invite"
    s.connect((HOST, PORT))
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
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet"
    #
    #print(HOST,PORT)
   
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return "Not login yet"
    if(friend==None):
        if token!=None:
            cmd="accept-invite "+token
        else:
            cmd="accept-invite"
    elif(friend!=None and trash==None):
        if token!=None:
            cmd="accept-invite "+token+" "+friend
        else:
            cmd="accept-invite "+friend
    else:
        if token!=None:
            
            cmd="accept-invite "+token+" "+friend+" "+trash
        else:
            cmd="accept-invite "+friend+" "+trash
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"]
def list_friend(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return 1,"Not login yet"
    #
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return 1,"Not login yet"
    if(trash!=None):
        if token==None:
            cmd="list-friend "+trash
        else:
            cmd="list-friend "+token+" "+trash
    else:
        if token!=None:
            cmd="list-friend "+token
        else:
            cmd="list-friend"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def post(user,content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet"
    #
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return "Not login yet"
    if(content!=None):
        if token!=None:
            cmd="post "+token+" "+content
        else:
            cmd="post "+content
    else:
        if token!=None:
            cmd="post "+token
        else:
            cmd="post"
    #print(cmd)
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
def receive_post(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return 1,"Not login yet"
    #
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return 1,"Not login yet"
    if(trash!=None):
        if token==None:
            cmd="receive-post "+trash
        else:
            cmd="receive-post "+token+" "+trash
    else:
        if token!=None:
            cmd="receive-post "+token
        else:
            cmd="receive-post"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["post"]
    else:
        return text["status"],text["message"]
def send(user,friend,msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet"
    #
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return "Not login yet"
    if friend!=None:
        if msg!=None:
            if token!=None:
                cmd="send "+token+" "+friend+" "+msg
            else:
                cmd="send "+friend+" "+msg
        else:
            if token!=None:
                cmd="send "+token+" "+friend
            else:
                cmd="send "+friend
    else:
        if msg!=None:
            if token!=None:
                cmd="send "+token+" "+msg
            else:
                cmd="send "+msg
        else:
            cmd="send"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
OUTPUT=""
class SampleListener(object,):
    def on_message(self, headers, message):
        #print ('headers: %s' % headers)
        print (message)
        #OUTPUT.write(message+'\n')
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
    
    HOST=login_HOST
    PORT=login_PORT
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
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet",1
    #
    
    
    
    token=""
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        #print(HOST,PORT)
        return "Not login yet",1
    if(group==None):
        if token!=None:
            cmd="create-group "+token
        else:
            cmd="create-group"
    elif(group!=None and trash==None):
        if token!=None:
            cmd="create-group "+token+" "+group
        else:
            cmd="create-group "+group
    else:
        if token!=None:
            cmd="create-group "+token+" "+group+" "+trash
        else:
            cmd="create-group "+group+" "+trash
    #print(cmd)
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"],text["status"]
def list_group(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return 1,"Not login yet"
    #
    
    token=""
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return 1,"Not login yet"
    if(trash!=None):
        if token==None:
            cmd="list-group "+trash
        else:
            cmd="list-group "+token+" "+trash
    else:
        if token!=None:
            cmd="list-group "+token
        else:
            cmd="list-group"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def list_joined(user,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
       # return 1,"Not login yet"
    #
    
    token=""
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return 1,"Not login yet"
    if(trash!=None):
        if token==None:
            cmd="list-joined "+trash
        else:
            cmd="list-joined "+token+" "+trash
    else:
        if token!=None:
            cmd="list-joined "+token
        else:
            cmd="list-joined"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    if(text["status"]==0):
        return text["status"],text["friend"]
    else:
        return text["status"],text["message"]
def join_group(user,group,trash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet",1
    #
    
    token=""
    """
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
    """
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
    except:
        token=None
        return "Not login yet",1
    if(group==None):
        if token!=None:
            cmd="join-group "+token
        else:
            cmd="join-group"
    elif(group!=None and trash==None):
        if token!=None:
            cmd="join-group "+token+" "+group
        else:
            cmd="join-group "+group
    else:
        if token!=None:
            
            cmd="join-group "+token+" "+group+" "+trash
        else:
            cmd="join-group "+group+" "+trash    
    s.connect((HOST, PORT))    
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()

    return text["message"],text["status"]
def send_group(user,group,msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    HOST=app_HOST
#    PORT=app_PORT
    #if check_login(user)=="no":
        #return "Not login yet"
    #
    
    cmd=""
    try:
        token=login_dict[user]
        HOST,PORT=app_conn_dict[user]
        #print(token)
    except:
        token=user
        return "Not login yet"
    if group!=None:
        if msg!=None:
            if token!=None:
                cmd="send-group "+token+" "+group+" "+msg
            else:
                cmd="send-group "+group+" "+msg
        else:
            if token!=None:
                cmd="send-group "+token+" "+group
            else:
                cmd="send-group "+group
    else:
        if msg!=None:
            if token!=None:
                cmd="send-group "+token+" "+msg
            else:
                cmd="send-group "+msg
        else:
            cmd="send-group"
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    text=json.loads(s.recv(1024).decode())
    s.close()
    return text["message"]
if __name__ == '__main__':

    #command=input("cmd:")
    subscribe_id_counter=0
    host=""
    port=int()
    INPUT=""

    if len(sys.argv) == 3:
        login_HOST=sys.argv[1]
        login_PORT=int(sys.argv[2])
        #INPUT=sys.argv[3]
        #OUTPUT=open(sys.argv[4],"w")

    thread_list=list()
    #HOST=input("IP:")
    #PORT=int(input("Port:"))

    while(1):
    #command="login 0410024 0410024"
    #for command in INPUT:
        #conn = stomp.Connection10([(activemq_host,activemq_port)])
    #while(1):
        #print(app_conn_dict)
        command=input()
        #command=command[:command.find("\n")]
        #print(command[:command.find("\n")])
        #cmd=command[:command.find(" ")]
        tmp=command.split()
        cmd=tmp[0]
        #print(command)
        #command=INPUT.getline
        output_msg=""
        if(cmd=="register"):
            msg=register(command)

            output_msg=msg+'\n'
            print(msg)

        elif(cmd=="login"):
            tmp=command.find(" ")

            user=command[tmp+1:command.find(" ",tmp+1)]
            status,msg,token,app_conn_addr,app_conn_port=login(command)
            app_HOST=app_conn_addr
            app_PORT=app_conn_port
            if(status==0):
                login_dict.update({user:token})
                app_conn_dict.update({user:(app_HOST,app_PORT)})
            #print(status,msg,token)
            output_msg=msg+'\n'
            #OUTPUT.writelines(output_msg)
            print(msg)

            if msg=="Success!":
                conn = stomp.Connection10([(login_HOST,activemq_port)])
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
                #conn.disconnect()

        elif(cmd=="logout"):
            user,trash=two_parameter(command)
            msg=logout(user,trash)
            output_msg=msg+'\n'
            print(msg)
            if msg=="Bye!":
                subscribe_delete_list=subscribe_dict[user]
                connect_delete=conn_dict[user]
                for a in subscribe_delete_list:
                    #connect_delete.start()
                    #connect_delete.connect()
                    connect_delete.unsubscribe(id=a)
                connect_delete.disconnect()
                del subscribe_dict[user]
                del conn_dict[user]
                del app_conn_dict[user]
        elif(cmd=="delete"):
            user,trash=two_parameter(command)
            msg=delete(user,trash)
            output_msg=msg+'\n'
            print(msg)
            if msg=="Success!":
                subscribe_delete_list=subscribe_dict[user]
                connect_delete=conn_dict[user]
                for a in subscribe_delete_list:
                    #connect_delete.start()
                    #connect_delete.connect()
                    connect_delete.unsubscribe(id=a)
                connect_delete.disconnect()
                del subscribe_dict[user]
                del conn_dict[user]
                del app_conn_dict[user]
        elif(cmd=="invite"):
            user,friend,trash=three_parameter(command)
            #print(user,friend,trash)
            msg=invite(user,friend,trash)
            output_msg=msg+'\n'
            print(msg)
        elif(cmd=="list-invite"):
            user,trash=two_parameter(command)
            status,msg=list_invite(user,trash)
            if(status==0):
                if len(msg)==0:
                    output_msg="No invitations"+'\n'
                    print("No invitations")
                else:
                    for i in msg:
                        output_msg+=i+"\n"
                        print(i)

            else:
                output_msg=msg+'\n'
                print(msg)
        elif(cmd=="accept-invite"):
            user,friend,trash=three_parameter(command)
            msg=accept_invite(user,friend,trash)
            output_msg=msg+'\n'
            print(msg)
        elif(cmd=="list-friend"):
            user,trash=two_parameter(command)
            status,msg=list_friend(user,trash)
            if(status==0):
                if len(msg)==0:
                    output_msg="No friends"+'\n'
                    print("No friends")
                else:
                    for i in msg:
                        output_msg+=i+"\n"
                        print(i)
            else:
                output_msg=msg+'\n'
                print(msg)
        elif(cmd=="post"):
            user,content=two_parameter(command)
            msg=post(user,content)
            output_msg=msg+'\n'
            print(msg)
        elif(cmd=="receive-post"):
            user,trash=two_parameter(command)
            status,msg=receive_post(user,trash)
            if(status==0):
                if len(msg)==0:
                    output_msg="No Posts"+'\n'
                    print("No Posts")
                else:
                    for i in msg:
                        output_msg+=i["id"]+":"+i["message"]+"\n"
                        print(i["id"]+":"+i["message"])
            else:
                output_msg=msg+'\n'
                print(msg)
        elif cmd=="send":
            user,friend,content=four_parameter(command)
            #print(user,friend,content)
            msg=send(user,friend,content)
            output_msg=msg+'\n'
            print(msg)
        elif cmd=="create-group":
            ###
            user,group,trash=three_parameter(command)
            msg,status=create_group(user,group,trash)
            output_msg=msg+'\n'
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
                    output_msg="No groups"+'\n'
                    print("No groups")
                else:
                    for i in msg:
                        output_msg+=i+"\n"
                        print(i)
            else:
                output_msg=msg+'\n'
                print(msg)
        elif cmd=="list-joined":
            user,trash=two_parameter(command)
            status,msg=list_joined(user,trash)
            if(status==0):
                if len(msg)==0:
                    output_msg="No groups"+'\n'
                    print("No groups")
                else:
                    for i in msg:
                        output_msg+=i+"\n"
                        print(i)
            else:
                output_msg=msg+'\n'
                print(msg)
        elif cmd=="join-group":
            ###
            user,group,trash=three_parameter(command)
            msg,status=join_group(user,group,trash)
            output_msg=msg+'\n'
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
            output_msg=msg+'\n'
            print(msg)
        else:
            if(command[0:4]=="exit"):
                #thread_list[0].delete()
                break
            else:
                output_msg=direct(command)+'\n'
                print(direct(command))
        #OUTPUT.write(output_msg)
        #OUTPUT.flush()
        #print(conn_dict)
        #print(subscribe_dict)
