#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# By L.F.Xie On 2017-02-07

import urllib2,urllib
import json
import hashlib
import time,datetime
import os,sys
import requests
import socket
import fcntl
import struct
import contacts

#返回当前时间的时间戳的java格式
def now_timestamp():
    localTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    startTimeArray = time.strptime(localTime, "%Y-%m-%d %H:%M:%S")
    startTimeStamp = int(time.mktime(startTimeArray))*1000
    return startTimeStamp


#登录json字典形式
login_json_dict = {"body":
                         {"username": "111111",
                          "channelCode": "test",
                          "userPwdMd5": "dc483e973673924"},
                    "head":
                         {"requestTime": now_timestamp(),
                          "sequenceCode": now_timestamp(),
                          "sourceSystem": "1"},
                    "sign": "aaaa"}


# 当前目录
def Get_File_Dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

LOG_DIR = Get_File_Dir()+'/log/'
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
    

# 网络接口IP地址
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

IPADDR = get_ip_address('eth0')

# 短信邮件报警
def Sms_Alert(Content,FileName,Status):
    Sms_Api = 'http://8.8.1.1/mail/sms.php'
    Title = '<BJ:XJ>dk::'+IPADDR+'::'+FileName+'::'+Status+'::'+Content
    #for User in Receiver_User:
    for User in contacts.Contacts():
        Post_Arg = '"notify_receiver='+User+'&user_name=test&user_passwd=test&notify_title='+Title+'&notify_body='+Content+'" '+Sms_Api
        Request = os.popen('curl -d ' + Post_Arg)

# 邮件报警
def Mail_Alert(Content,FileName,Status):
    Mail_Api = 'http://8.8.1.1/mail/mail.php'
    Title = '<BJ:XJ>dk::'+IPADDR+'::'+FileName+'::'+Status+'::'+Content
    #for User in Receiver_User:
    for User in contacts.Contacts():
        Post_Arg = '"notify_receiver='+User+'&user_name=test&user_passwd=test&notify_title='+Title+'&notify_body='+Content+'" '+Mail_Api
        Request = os.popen('curl -d ' + Post_Arg)


# 生成字符串的md5值
def md5Util(str_arg):
    m2 = hashlib.md5()
    m2.update(str_arg)
    return m2.hexdigest()

# 日志文件
def logUtil(Body):
    Date = time.strftime("%Y-%m-%d",time.localtime())
    Log_File = Get_File_Dir()+'/log/'+Date+'.log'
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    with open(Log_File,'a') as f:
        f.write("["+NowTime+"] "+Body+"\n")

# 日志工具类
def logUtil_1(content):
    log_name = time.strftime("%Y-%m-%d",time.localtime())+".log"
    #file_path = os.path.join(".",log_name)
    file_path = os.path.join(log_path,log_name)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    timePre = "["+now_time+"]"
    input_content = timePre+content+"\n"
    with open(file_path,"a") as f:
        f.write(input_content)

# 登陆
def Get_Login_Info():
    LOGIN_URL = 'https://test.1234.com/Service/'
    #获取登录信息
    logUtil("-------------------【api监控-登录】")
    #global start_time
    start_time = datetime.datetime.now()
    sign = md5Util(json.dumps(login_json_dict))
    login_json_dict["sign"] = sign
    login_data = {}
    login_data["p"] = json.dumps(login_json_dict)
    #s = json.dumps(p)
    login_data = urllib.urlencode(login_data)
    login_req = urllib2.Request(LOGIN_URL, login_data)
    login_response = urllib2.urlopen(login_req)
    login_the_page = login_response.read()
    login_respose_dict = json.loads(login_the_page)
    #print login_respose_dict
    login_end_time = datetime.datetime.now()
    #如果时间大于1秒取秒值，如果时间小于一秒取毫秒值
    if (login_end_time-start_time).seconds>1:
        logUtil("登录用时:%s" % str((login_end_time-start_time).seconds)+"s")
    else:
        logUtil("登录用时:%s" % str(((login_end_time-start_time).microseconds)/1000)+"ms")
    try:
        status = login_respose_dict["head"]["status"]
        if status == '0':
            userId = login_respose_dict["body"]["userInfo"]["userId"]
            #print '-------- userId: %s' % userId
            #print type(userId)
            #sys.exit()
            token = login_respose_dict["body"]["token"]
            uaaId = login_respose_dict["body"]["userInfo"]["uaaId"]
            phone = login_respose_dict["body"]["userInfo"]["phone"]
            logUtil("登录请求成功:status == 0")
            INFO_DICT = {'userId':userId,'token':token,'phone':phone,'uaaId':uaaId}
            return str(INFO_DICT)
        else:
            logUtil("登录请求json:%s" % json.dumps(login_json_dict))
            logUtil("登录返回JSON:%s" % login_the_page)
            logUtil("【api监控-登录】status!=0,error:%s" % login_respose_dict["head"]["errorMessage"])
            Mail_Alert("【api监控-登录】status!=0,error:%s" % login_respose_dict["head"]["errorMessage"])
            end_time = datetime.datetime.now()
            if (end_time-start_time).seconds>1:
                return str((end_time-start_time).seconds)+"s"
            else:
                return str(((end_time-start_time).microseconds)/1000)+"ms"
    except Exception as e:
        logUtil("登录请求json:%s" % str(login_json_dict))
        logUtil("登录返回JSON:%s" % login_the_page)
        logUtil("【api监控-登录】登录参数解析错误:%s" % e)
        Mail_Alert("【api监控-登录】参数解析错误:%s" % e)
        end_time = datetime.datetime.now()
        if (end_time-start_time).seconds>1:
            return str((end_time-start_time).seconds)+"s"
        else:
            return str(((end_time-start_time).microseconds)/1000)+"ms"
