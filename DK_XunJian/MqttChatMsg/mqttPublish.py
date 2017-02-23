#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By L.F.Xie On 2017-02-20

# 该脚本用户检测mqtt聊天消息功能的发布功能,另一脚本为验证订阅功能,两个必须一起使用.

import sys
sys.path.append("..")
import public.public as public
#import public.conn as conn
import time
import paho.mqtt.client as mqtt
import datetime
import socket
import os

API_NAME = 'Mqtt 聊天消息发布'
API_URL = '127.0.0.1'
API_PORT = 1883
user = 'ap_mo_ur'
pwd = '4eqaTrupre'
TOPIC = 'TOPIC_ChJian'
Test_Msg = 'MSG_DunJian'

IPADDR = public.get_ip_address('eth0')
MYSELF_NAME = '[XJ]%s' % os.path.basename(__file__)

def on_publish(msg, rc):
    if rc == 0:
        CONT = '%s巡检 [ OK ], publish msg is: [%s]' % (API_NAME,msg)
        public.logUtil(CONT)
        public.Mail_Alert(CONT, MYSELF_NAME, 'OK')
        print("publish success, msg = " + msg)
    else:
        CONT = '%s巡检 [ ERROR ], publish msg is failed.' % API_NAME
        public.logUtil(CONT)
        public.Sms_Alert(CONT, MYSELF_NAME, 'CRITICAL')
        print("Error, publish failed.")

def on_connect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    if rc == 0:
        CONT = 'OK, Connect success, rc=0.'
        public.logUtil(CONT)
        print("[ OK ] Connect success.")
    else:
        CONT = '[ ERROR ] Connect failed, rc=%s.' % rc
        public.logUtil(CONT)
        print("Error, Connect failed.")


try:
    client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.username_pw_set(user, pwd)
    client.connect(API_URL, API_PORT, keepalive=60)
    client.on_connect = on_connect
    client.loop_start()
    time.sleep(2)
    count = 0
    
    while count < 1:
    #while True:
        count = count + 1
        #msg = str(datetime.datetime.now())
        msg = Test_Msg
        rc , mid = client.publish(TOPIC, payload=msg, qos=1)
        on_publish(msg, rc)
        #time.sleep(10)
except Exception as e:
    CONT = '[巡检-聊天消息]Mqtt链接服务器异常,Error: %s' % e
    public.logUtil(CONT)
    print CONT
    public.Sms_Alert(CONT, MYSELF_NAME, 'CRITICAL')
    client.disconnect()
