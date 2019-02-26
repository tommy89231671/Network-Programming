# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:19:09 2018

@author: tommy
"""

import socket
import uuid
import json
from peewee import *
from peewee import CharField
from peewee import MySQLDatabase
from peewee import Model

mysql_db = MySQLDatabase('NP', user='tommy', password='123',host='140.113.67.107', port=3306)



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
Invite.delete().where((Invite.user_me=="gakki")|(Invite.user_invite=="gakki")).execute()
#Friend.delete().where((Friend.me=="gakki")|(Friend.friend=="gakki")).execute()
#query=Friend.select(Friend.friend,Post.post).join(Post,on=(Friend.friend==Post.user)).where(Friend.me=='gakki').dicts()
#for row in query:
#    row['id'] = row.pop('friend')
#    row['message'] = row.pop('post')
#    print(row)
#a="register"
#b=a.split()


#print(' '.join(b))
##
HOST = '10.0.2.15'
PORT = 3306
#
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    cmd=input("cmd:")
    s.send(cmd.encode())
    #if(cmd=="exit"):
    #    break
    #resp = s.recv(4096).decode()
    #print(resp)
