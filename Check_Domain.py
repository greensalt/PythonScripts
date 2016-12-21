#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Xie.L.F On 2016-12-21

'''
该脚本用于检测平台域名解析变更,如果有变更则发通知.
'''

import os,time
import dns.resolver
import socket
import fcntl
import struct

# DomainName List:
DomainNames = ['test.test.com',
               'test2.test.com'
              ]

# Alert Contacts:
Mail_User = ['aaaa@163.com',
             'bbb@163.com'
            ]
# 去重:
Receiver_User = list(set(Mail_User))

Alert_Api = 'http://a.t.com/api'

Date = time.strftime("%Y-%m-%d",time.localtime())
Log_File = '/tmp/Check_Domain'+Date+'.log'

my_resolver = dns.resolver.Resolver()
#my_resolver.nameservers = ['8.8.8.8']
my_resolver.nameservers = ['192.168.100.88']

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def Alert(Body):
    IPADDR = get_ip_address('eth0')
    Title = '<BJ:CUS>hy_03::'+IPADDR+'::Check_DomainName::WARNING::'+Body
    for User in Receiver_User:
        Post_Arg = 'notify_receiver='+User+'&user_name=nagios&user_passwd=123456&notify_title='+Title+'&notify_body='+Body
        Request = os.popen('curl -d "' + Post_Arg + '" ' + Alert_Api)

def Write_Log(Body):
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    with open(Log_File,'a') as f:
        f.write("["+NowTime+"] "+Body+"\n")

def Write_Temp_File(DM,IP):
    Temp_File = '/tmp/'+DM+'.tmp'
    with open(Temp_File,'wr') as f:
        f.write(IP)

def Read_Temp_File(DM):
    Temp_File = '/tmp/'+DM+'.tmp'

    try:
        with open(Temp_File) as f:
            IP = f.read()
    except IOError:
        Write_Log('[ Error ]'+Temp_File+' is not exist.')
    else:
        return IP


def Query_DM(DomainName_List):
    for DomainName in DomainName_List:
        File_Tmp = '/tmp/'+DomainName+'.tmp'
        #New_IP = dns.resolver.query(DomainName,'A')
        New_IP_Class = my_resolver.query(DomainName,'A')

        for i in New_IP_Class.response.answer:
            for j in i.items:
                New_IP = str(j.to_text())

        if os.path.isfile(File_Tmp):
            Old_IP = Read_Temp_File(DomainName)
            #import pdb
            #pdb.set_trace()
        else:
            Write_Temp_File(DomainName,New_IP)
            Write_Log('[ First ] %s: %s' % (DomainName,New_IP))
            continue
            
        if New_IP != Old_IP:
            Content = '['+DomainName+']:'+'New_IP:'+New_IP+' Old_IP:'+Old_IP
            Write_Log('[ Warning ]'+Content)
            Write_Temp_File(DomainName,New_IP)
            Alert(Content)
        else:
            Content = '%s:%s' % (DomainName,New_IP)
            Write_Log(Content)


if __name__ == '__main__':
    Write_Log('-'*50)
    Query_DM(DomainNames)
