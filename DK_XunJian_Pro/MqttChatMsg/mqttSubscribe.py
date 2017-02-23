#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By L.F.Xie On 2017-02-20

# 该脚本用户检测mqtt聊天消息功能的订阅功能,另一脚本为验证发布功能,两个必须一起使用.

import sys
sys.path.append("..")
import paho.mqtt.client as mqtt
import json
import time
import public.public as public
#import public.conn as conn
import os
#import threading

API_NAME = 'Mqtt 聊天消息订阅'
API_URL = '127.0.0.1'
API_PORT = 1883
user = 'ap_mo_ur'
pwd = '4eqaTrupre'
TOPIC = 'TOPIC_ChJian'
Test_Msg = 'MSG_DunJian'

IPADDR = public.get_ip_address('eth0')
MYSELF_NAME = '[XJ]%s' % os.path.basename(__file__)


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    #S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    MSG = str(msg.payload)
    MSG_TOPIC = msg.topic
    print MSG_TOPIC + ' ' + MSG

    if MSG == Test_Msg:
        CONT = '%s巡检 [ OK ], subscribe msg is: [%s]' % (API_NAME, MSG)
        public.logUtil(CONT)
        print CONT
        public.Mail_Alert(CONT, MYSELF_NAME, 'OK')
        #Status = '0'
    else:
        CONT = '%s巡检 [ ERROR ], subscribe msg is: [%s], but get msg is: [%s]' % (API_NAME, Test_Msg, MSG)
        public.logUtil(CONT)
        print CONT
        public.Sms_Alert(CONT, MYSELF_NAME, 'CRITICAL')
        #Status = '1'
    #E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    #conn.Insert_DB(API_NAME,'%s:%s' % (API_URL,API_PORT),'Null','Null',Status,IPADDR,S_TIME,E_TIME)
    #print API_NAME,'%s:%s' % (API_URL,API_PORT),'Null','Null',Status,IPADDR,S_TIME,E_TIME
    

if __name__ == '__main__':
    # 创造线程:
    #t = threading.Thread(target=on_connect)
    #t.setDaemon(True)
    #t.start()

    client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.username_pw_set(user, pwd)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(API_URL, port=API_PORT, keepalive=60)
        client.loop_forever()
    except Exception as e:
        CONT = '[巡检-聊天消息]Mqtt链接服务器异常,Error: %s' % e
        public.logUtil(CONT)
        print CONT
        public.Sms_Alert(CONT, MYSELF_NAME, 'CRITICAL')
        client.disconnect()
