#!/usr/bin/python
# -*- coding: utf-8 -*-
# By xielifeng On 2017-01-06
 
import urllib2
import os,sys
import time
import socket
import fcntl
import struct

# Alert Contacts:
Mail_User = ['xielifeng@sinoiov.com',
            ]
# 去重:
Receiver_User = list(set(Mail_User))

Alert_Api = 'http://58.83.210.31:8866/mail_sms/sms.php'
Date = time.strftime("%Y-%m-%d",time.localtime())
Log_File = '/tmp/Check_html_api_'+Date+'.log'
 
URLS_D = {
    '加油':'https://card-mobile.95155.com/ypptMobileApp/index.html',
    '商城':'https://test-appapis.95155.com/mall-mobile-api/mall8/index.html',
    '二手车':'https://test-vehiclesales.95155.com/vehicle-sales-web/toIndex',
    'ETC':'http://test.mobile.api.etc.95155.com:8085/etc-mobile-api/pages/index.html',
    '找车':'https://wxbeta.95155.com/vehicles.html',
    '找货':'http://wxbeta.95155.com/index.html',
    '记账本':'https://test-appapis.95155.com/cashbook-mobile-api/cashbook/account_book.html',
    '违章查询':'http://test-appapis.gghypt.net/base-mobile-api/wzcx.html',
    '我的钱包':'http://card-mobile.95155.com/payMobileApp/wallet/index.html'
}
#url = 'https://card-mobile.95155.com/ypptMobileApp/index22.html'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def Alert(Body):
    IPADDR = get_ip_address('eth0')
    if 'Error' in Body:
        Alert_level = 'CRITICAL'
    elif 'Ok' in Body:
        Alert_level = 'Ok'
    else:
        Alert_level = None
    Title = '<BJ:CUS>daka::'+IPADDR+'::Check_html_api::'+Alert_level+'::'+Body
    for User in Receiver_User:
        Post_Arg = 'notify_receiver='+User+'&user_name=nagios&user_passwd=nagios&notify_title='+Title+'&notify_body='+Body
        Request = os.popen('curl -d "' + Post_Arg + '" ' + Alert_Api)

def Write_Log(Body):
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    with open(Log_File,'a') as f:
        f.write("["+NowTime+"] "+Body+"\n")

def Check_api():
    for key,url in URLS_D.items():
        #print key,'---',url
        response = None
        try:
            response = urllib2.urlopen(url,timeout=10)
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                Content = '%s:[ Error ]:%s' % (key,e.code)
                print Content
                Write_Log(Content)
                Alert(Content)
            elif hasattr(e, 'reason'):
                Content = 'Reason:[ Error ]:%s' % e.reason
                print Content
                Write_Log(Content)
                Alert(Content)
        finally:
            if response:
                Content = '%s:[ Ok ]' % key
                print Content
                Write_Log(Content)
                Alert(Content)
                response.close()

if __name__ == '__main__':
    Write_Log('-'*50)
    Check_api()
