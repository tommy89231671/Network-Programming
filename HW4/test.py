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
host='172.20.10.2'


class SampleListener(object):
    def on_message(self, headers, message):
        print ('headers: %s' % headers)
        print ('message: %s' % message)

# 推送到隊列queue
def send_to_queue(msg):
    conn = stomp.Connection10([(host,port)])
    conn.start()
    conn.connect()
    conn.send(queue_name, msg)
    conn.disconnect()

#推送到主題
def send_to_topic(msg):
    conn = stomp.Connection10([(host,port)])
    conn.start()
    conn.connect()
    conn.send(topic_name, msg)
    conn.disconnect()

##從隊列接收消息
def receive_from_queue():
    conn = stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(queue_name)
    time.sleep(1) # secs
    conn.disconnect()

##從主題接收消息
def receive_from_topic():
    conn = stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(topic_name)
    while 1:
        send_to_topic('topic')
        time.sleep(3) # secs
    conn.disconnect()

if __name__=='__main__':
    #send_to_queue('len 123')
    #receive_from_queue()
    #send_to_topic('len 345')
    #receive_from_topic()
    conn = stomp.Connection10([(host,port)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    print(conn.subscribe(destination=queue_name,id=123))
    #conn.unsubscribe(destination=queue_name,id=2)
    #time.sleep(1) # secs
    input()
    conn.disconnect()
import stomp
queue_name = '/queue/SampleQueue'
topic_name = '/topic/SampleTopic1'
listener_name = 'SampleListener'
port=61613
host='172.20.10.2'


class SampleListener(object):
    def on_message(self, headers, message):
        print ('headers: %s' % headers)
        print ('message: %s' % message)

conn = stomp.Connection10([(host,port)])
conn.set_listener(listener_name, SampleListener())
conn.start()
conn.connect()
conn.subscribe(destination=queue_name,id=123)
#conn.unsubscribe(destination=queue_name,id=2)
#time.sleep(1) # secs
input()
conn.disconnect()
