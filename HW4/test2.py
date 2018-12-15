# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:54:08 2018

@author:
"""

# -*-coding:utf-8-*-
import stomp
import time


queue_name = '/queue/SampleQueue'
topic_name = '/topic/SampleTopic1'
listener_name = 'SampleListener'
port=61613
host="172.20.10.2"


class SampleListener(object):
    def on_message(self, headers, message):
        print ('headers: %s' % headers)
        print ('message: %s' % message)

# 推送到隊列queue
def send_to_queue(msg):
    conn = stomp.Connection10([(host,port)])
    conn.start()

    conn.connect()
    print("yes")
    conn.send(queue_name, msg)

    conn.disconnect()

#推送到主題
#conn = stomp.Connection10([(host,port)])
def send_to_topic(msg):
    conn = stomp.Connection10([(host,port)])
    conn.start()
    conn.connect()
    #txid = conn.begin()
    #conn.send(topic_name, msg)
    conn.subscribe(destination="/topic/1211211")
    #conn.abort(txid)
    conn.disconnect()

##從隊列接收消息
#conn = stomp.Connection10([(host,port)])
conn_list=list()
def receive_from_queue():
    #conn = stomp.Connection10([(host,port)])
    conn=stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    #print("wait")
    conn.subscribe(destination=queue_name,id=2)

    conn_list.append(conn)
    #time.sleep(1) # secs
    conn.disconnect()

##從主題接收消息
def receive_from_topic():
    conn = stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(topic_name)


        #send_to_topic('topic')
        #time.sleep(3) # secs
    conn.disconnect()
    input()
if __name__=='__main__':
    #while 1:
    #send_to_queue('abc')
    #send_to_queue('ssd')
    #print("abc")
    #while 1:
    #input(" ")
    """receive_from_queue()
    while 1:
    input(" ")
    conn=stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    #print("wait")
    conn.subscribe(destination=queue_name,id=2)
    conn_list.append(conn)
    #time.sleep(1) # secs
    conn.disconnect()


    conn = conn_list[0]
    conn.start()
    conn.connect()
    conn.unsubscribe(destination=queue_name,id=1)
    conn.disconnect()
    input(" ")"""
    #send_to_topic('len 345')


    receive_from_topic()

        #
    #input(" ")
