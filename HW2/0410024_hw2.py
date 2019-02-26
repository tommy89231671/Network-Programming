# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:34:48 2018

@author: tommy
"""

import socket
import json
import sys
HOST = ""
PORT = ""
login_dict=dict()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
if __name__ == '__main__':
    
    #command=input("cmd:")
    host=""
    port=int()
    if len(sys.argv) == 3:
        HOST=sys.argv[1]
        PORT=int(sys.argv[2])
    
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
            
        elif(cmd=="logout"):
            user,trash=two_parameter(command)
            msg=logout(user,trash)
            print(msg)
        elif(cmd=="delete"):
            user,trash=two_parameter(command)
            msg=delete(user,trash)
            print(msg)            
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
        else:
            if(command[0:4]=="exit"):
                break
            else:
                print(direct(command))
            
        
    
    
    
    
    
    