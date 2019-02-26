# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:49:28 2018

@author: tommy
"""
#import  pymysql

import os
from peewee import *
from peewee import CharField
from peewee import IntegerField
from peewee import MySQLDatabase
from peewee import Model
from playhouse.db_url import connect
import socket
import uuid
import json
import sys
import stomp
import boto3
import time
import requests
import traceback
response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
login_iid = response.text



conn=stomp.Connection10()

#import secrets
activemq_host="0.0.0.0"
mysql_host="npdbinstance.clvibnzutilv.us-east-1.rds.amazonaws.com"
activemq_port=61613
mysql_db = MySQLDatabase('np', user='tommy', password='123456789',host=mysql_host, port=3306)
#mysql_db.connect()
host=""
port=int()
app_conn_init_port=22222

if len(sys.argv) == 3:
    host=sys.argv[1]
    port=int(sys.argv[2])



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((host, port))

serversocket.listen(5)

instances_dict=dict()
instances_list=list()

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
    app_server_addr=CharField(default='')
    app_server_port=IntegerField(default=0)
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
        
def app_server_assign():
    ec2 = boto3.resource('ec2')
    th=ec2.Instance(login_iid)
    this_addr=th.public_ip_address
    
    user_data="""#!/bin/bash
    /home/ubuntu/anaconda3/bin/python3 /home/ubuntu/app_server.py 0.0.0.0 22222 """+this_addr
    #user_data+=
    ec2 = boto3.resource('ec2', region_name = 'us-east-1')
    a=ec2.create_instances(
        BlockDeviceMappings=[
          {
              'DeviceName':"/dev/sda1",
              'Ebs':{
                  'DeleteOnTermination':True,
    	      #'SnapshotId':'snap-07a5307a919c1486b'	
              }
          }
        ],
        ImageId='ami-07077b75d639ddc57', 
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
    	    'Groups': ["sg-0bf4d9509f30873e7"],
                
                'SubnetId': 'subnet-d9690ff7'
            }
        ],
        MinCount=1, 
        MaxCount=1,
        KeyName='ec2_key',
        
        InstanceType="t2.micro",
    
        UserData=user_data
    )
    
    
    iid=a[0].instance_id
    #print(iid)
    time.sleep(3)
    b=ec2.Instance(iid)
    time.sleep(20)
    
    return iid,b.public_ip_address
try:
    while True:
    
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        (clientsocket, address) = serversocket.accept()
        #print(clientsocket,address)
        command=clientsocket.recv(1024).decode()
        #cmd=command[:command.find(" ")]
        tmp=command.split()
        cmd=tmp[0]
        print(instances_list)
        print(instances_dict)
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
                a=User.select(User.account,User.password,User.token,User.app_server_addr,User.app_server_port).where(User.account==user,User.password==pw).dicts()
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
                    print(token)
                    User.update(**{"token": token}).where(User.account==user,User.password==pw).execute()
                    #######Instance job#########
                    app_conn_addr=""
                    app_conn_port=22222
                    app_iid=""
                    if len(instances_list)==0:
                        app_iid,app_conn_addr=app_server_assign()
                        #app_conn_port=app_conn_init_port
                        
                        instances_list.append((app_iid,app_conn_addr))
                        instances_dict.setdefault(app_conn_addr,1)
                    else:
                        flag=0 #all full or not
                        for inst in instances_list:
                            if instances_dict[inst[1]]<10:
                                app_conn_addr=inst[1]
                                #app_conn_port=app_conn_init_port+instances_dict[inst]
                                instances_dict[inst[1]]+=1
                                flag=1
                                break
                            else:
                                flag=0
                            #elif instances_dict[inst]
                        if flag==0:
                            app_iid,app_conn_addr=app_server_assign()
                            #app_conn_port=app_conn_init_port
                            instances_list.append((app_iid,app_conn_addr))
                            instances_dict.setdefault(app_conn_addr,1)
                    print('app:'+app_conn_addr,app_conn_port)
                    User.update(**{"app_server_addr": app_conn_addr}).where(User.account==user,User.password==pw).execute()
                    User.update(**{"app_server_port": app_conn_port}).where(User.account==user,User.password==pw).execute()
                    server_json=json.dumps({ 'status': 0,'token':token ,'message': "Success!",'app_conn_addr':app_conn_addr,'app_conn_port':app_conn_port}, sort_keys=True, indent=4, separators=(',', ': '))
    
                elif row["token"]!="":
                    token=row["token"]
                    app_conn_addr=row["app_server_addr"]
                    app_conn_port=row["app_server_port"]
                    #print("success")
                    server_json=json.dumps({ 'status': 0,'token':token ,'message': "Success!",'app_conn_addr':app_conn_addr,'app_conn_port':app_conn_port}, sort_keys=True, indent=4, separators=(',', ': '))
    
            else:
                #print("usage wrong")
                server_json=json.dumps({ 'status': 1,'message': "Usage: login <id> <password>"}, sort_keys=True, indent=4, separators=(',', ': '))
    
        elif cmd=="logout":
            status,token=one_parameter(command)
            msg=""
            msg_status=0
            if status==0:
                row=dict()
                a=User.select(User.account,User.password,User.token,User.app_server_addr,User.app_server_port).where(User.token==token).dicts()
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
                    instances_dict[row["app_server_addr"]]-=1
                    if instances_dict[row["app_server_addr"]]==0:
                        
                        del instances_dict[row["app_server_addr"]]
                        
                        
                        
                        
                        for i,a in enumerate(instances_list):
                            if a[1]==row["app_server_addr"]:
                                client = boto3.client('ec2')
                                client.terminate_instances(InstanceIds=[a[0]])
                                instances_list.pop(i)
                                print(a[1]+" shut down")
                    User.update(**{"token": ""}).where(User.account==row["account"]).execute()
                    User.update(**{"app_server_addr": ""}).where(User.account==row["account"]).execute()
                    User.update(**{"app_server_port": 0}).where(User.account==row["account"]).execute()
                    
                   
                                
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
                a=User.select(User.account,User.password,User.token,User.app_server_addr,User.app_server_port).where(User.token==token).dicts()
                try:
                    row=a[0]
                except:
                    row=dict()
                if len(row)==0:
                    #print("not login yet")
                    msg="Not login yet"
                    msg_status=1
                else:
                    instances_dict[row["app_server_addr"]]-=1
                    if instances_dict[row["app_server_addr"]]==0:
                        del instances_dict[row["app_server_addr"]]
                        for i,a in enumerate(instances_list):
                            if a[1]==row["app_server_addr"]:
                                client = boto3.client('ec2')
                                client.terminate_instances(InstanceIds=[a[0]])
                                instances_list.pop(i)
                                print(a[1]+" shut down")
                    Invite.delete().where((Invite.user_me==row["account"])|(Invite.user_invite==row["account"])).execute()
                    Friend.delete().where((Friend.me==row["account"])|(Friend.friend==row["account"])).execute()
                    Post.delete().where(Post.user==row["account"]).execute()
                    User.delete().where(User.account==row["account"]).execute()
                    Club.delete().where(Club.member==row["account"]).execute()
                    #print("Bye")
                    
                   
                    
                    msg="Success!"
                    msg_status=0
        
            
            else:
                #print("usage wrong")
                msg="Usage: delete <user>"
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
        elif cmd=="Check_login":
            #print("check now")
            space=command.find(" ")
            user=command[space+1:]
            row=dict()
            query1=User.select().where(User.account==user).dicts()
            try:
                row=query1[0]
                server_json=json.dumps({ 'status': 'yes'}, sort_keys=True, indent=4, separators=(',', ': '))
            except:
                row=dict()
                server_json=json.dumps({ 'status': 'no'}, sort_keys=True, indent=4, separators=(',', ': '))
    #        try:
    #            a=row['token']
    #            server_json=json.dumps({ 'status': 'yes'}, sort_keys=True, indent=4, separators=(',', ': '))
    #        except:
    #            server_json=json.dumps({ 'status': 'yes'}, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            server_json=json.dumps({ 'status': 1,'message': "Unknown command "+cmd}, sort_keys=True, indent=4, separators=(',', ': '))
        clientsocket.send(server_json.encode())
        
except Exception as e:
    error_class = e.__class__.__name__ #
    detail = e.args[0]
    cl, exc, tb = sys.exc_info()
    lastCallStack = traceback.extract_tb(tb)[-1] 
    fileName = lastCallStack[0] 
    lineNum = lastCallStack[1] 
    funcName = lastCallStack[2] 
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)

    """
    login gakki 123
    login satomi 123
    send gakki satomi wewewewe

    """
