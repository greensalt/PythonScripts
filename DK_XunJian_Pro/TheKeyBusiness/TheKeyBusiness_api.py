#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# By L.F.Xie On 2017-02-07

import os,sys
sys.path.append("..")
import public.public as public
import requests
import json
import time
import public.conn as conn

# 获取用户信息
LOGIN_RESULT_DICT = eval(public.Get_Login_Info())
USER_TOKEN = LOGIN_RESULT_DICT['token']
USER_USERID = LOGIN_RESULT_DICT['userId']
USER_UAAID = LOGIN_RESULT_DICT['uaaId']
USER_MOBILE = LOGIN_RESULT_DICT['phone']

# 定义报警内容列表
OK_RESULT = []
ERR_RESULT = []

MYSELF_NAME = '[XJ]%s' % os.path.basename(__file__)
IPADDR = public.get_ip_address('eth0')
TIMEOUT = 10

#  1
def Second_Hand_Car():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    API_NAME = '二手车'
    API_URL = 'https://test.1234.com/'
    REQ_PAR = {'paren': '80'}

    try:
        r = requests.post(API_URL, data=REQ_PAR, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)

        if JSON_DATA['data']:
            CONT = '%s巡检 [ OK ].' % API_NAME
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].' % API_NAME
            public.logUtil(CONT)
            ERR_RESULT.append(API_NAME)
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str(REQ_PAR),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# 找车|找货 2
def Find_Car_Goods():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    FIND_CAR_GOODS_API = {
                          '找车':'https://test.123.com/',
                          '找货':'https://test.123.com/'
                         }
    REQ_PAR = {}
    for API_NAME,API_URL in FIND_CAR_GOODS_API.items():
        try:
            r = requests.post(API_URL, timeout=TIMEOUT)
            JSON_DATA = json.loads(r.text)
            if JSON_DATA['status'] == 1001:
                CONT = '%s巡检 [ OK ].' % API_NAME
                public.logUtil(CONT)
                OK_RESULT.append(API_NAME)
                Status = '0'
            else:
                CONT = '%s巡检 [ ERROR ].' % API_NAME
                public.logUtil(CONT)
                ERR_RESULT.append(API_NAME)
                Status = '1'
        except requests.exceptions.RequestException as e:
            CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
            JSON_DATA = e
            public.logUtil(CONT)
            ERR_RESULT.append('%s {%s}' % (API_NAME,e))
            Status = '1'

        E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
        conn.Insert_DB(API_NAME,API_URL,str(REQ_PAR),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# 2
def Check_Tally_Book():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    NOW_TIME = unicode(time.strftime("%Y%m",time.localtime()),"utf-8")
    API_NAME = '记账本'
    API_URL = 'https://test.123.com/'
    REQ_PAR = {'userId':USER_USERID,
               'startTime': NOW_TIME,
               'endTime': NOW_TIME}

    try:
        r = requests.post(API_URL, data=REQ_PAR, verify=False, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)

        if int(JSON_DATA['status']) == 0:
            CONT = '%s巡检 [ OK ].' % API_NAME
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].' % API_NAME
            public.logUtil(CONT)
            ERR_RESULT.append(API_NAME)
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str(REQ_PAR),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# ETC (code返回值小于0失败,大于0为成功)
def Check_Etc():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    API_NAME = 'ETC'
    API_URL = 'http://test.123.com/'
    REQ_PAR = {
                  "head": {
                      "uaaId": USER_UAAID,
                      "userId": USER_USERID,
                      "token": "",
                      "sequenceCode": "5b21d75d",
                      "mobileNo": USER_MOBILE,
                      "sequenceNum": "14801"
                  },
                  "body": {},
                  "sign": "1111"
             }

    sign = public.md5Util(json.dumps(REQ_PAR))
    REQ_PAR['sign'] = sign

    try:
        r = requests.post(API_URL, data=json.dumps(REQ_PAR), headers = {"Content-Type": "application/json;charset=utf-8"}, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)
        CODE_RESULT = JSON_DATA['body']['code']

        if CODE_RESULT >= 0:
            CONT = '%s巡检 [ OK ]. code == %s' % (API_NAME,CODE_RESULT)
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].code == %s' % (API_NAME,CODE_RESULT)
            public.logUtil(CONT)
            ERR_RESULT.append('%s, code == %s' % (API_NAME,CODE_RESULT))
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str(REQ_PAR),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# 钱包
def Wallet():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    API_NAME = '钱包'
    API_URL = 'https://test.123.com/'
    REQ_PAR = {"head":
                  {"servCode": "Z000006",
                   "mobileNo": "",
                   "sequenceNum": "1484545380337"},
               "body":
                  {"userId": USER_USERID,
                   "tokenId": USER_TOKEN},
               "sign": "Z123"}

    sign = public.md5Util(json.dumps(REQ_PAR).replace(" ",""))
    REQ_PAR['sign'] = sign

    try:
        r = requests.post(API_URL, data=json.dumps({"param": REQ_PAR}), headers = {"Content-Type": "application/x-www-form-urlencoded"}, verify=False, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)

        if int(JSON_DATA['head']['result']) == 0:
            CONT = '%s巡检 [ OK ].' % API_NAME
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].' % API_NAME
            public.logUtil(CONT)
            ERR_RESULT.append(API_NAME)
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str({"param":REQ_PAR}),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# 商城
def Mall():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    API_NAME = '商城'
    API_URL = 'https://test.123.com/'
    REQ_PAR = {
                  "head": {
                      "userId": USER_USERID,
                      "token": USER_TOKEN,
                      "mobileNo": "",
                      "sequenceNum": "1480"
                  },
                  "body": {
                      "pageNum": 12,
                      "pageSize": 1
                  },
                  "sign": "1331"
             }


    sign = public.md5Util(json.dumps(REQ_PAR))
    REQ_PAR['sign'] = sign

    try:
        r = requests.post(API_URL, data={"p": json.dumps(REQ_PAR)}, headers = {"Content-Type": "application/x-www-form-urlencoded"}, verify=False, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)

        if int(JSON_DATA['head']['status']) == 0:
            CONT = '%s巡检 [ OK ].' % API_NAME
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].' % API_NAME
            public.logUtil(CONT)
            ERR_RESULT.append(API_NAME)
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str(REQ_PAR),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)

# 油品移动端  首页开卡列表查询
def MobileApp_First_Page():
    S_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    API_NAME = '油品移动端首页开卡列表查询'
    API_URL = 'http://test.123.com/'
    REQ_PAR = {"head":
                  {"callTime":"1484741",
                   "sequenceNum":"1480741"},
               "body":
                  {"tokenId":"您好",
                   "userId":USER_USERID,
                   "page":1,
                   "row":2},
               "sign":"Z123&"}

    sign = public.md5Util(json.dumps(REQ_PAR))
    REQ_PAR['sign'] = sign

    try:
        r = requests.post(API_URL, data={"params": json.dumps(REQ_PAR)}, timeout=TIMEOUT)
        JSON_DATA = json.loads(r.text)

        if int(JSON_DATA['head']['result']) == 0:
            CONT = '%s巡检 [ OK ].' % API_NAME
            public.logUtil(CONT)
            OK_RESULT.append(API_NAME)
            Status = '0'
        else:
            CONT = '%s巡检 [ ERROR ].' % API_NAME
            public.logUtil(CONT)
            ERR_RESULT.append(API_NAME)
            Status = '1'
    except requests.exceptions.RequestException as e:
        CONT = '%s巡检 [ ERROR ].%s' % (API_NAME,e)
        JSON_DATA = e
        public.logUtil(CONT)
        ERR_RESULT.append('%s {%s}' % (API_NAME,e))
        Status = '1'

    E_TIME = unicode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"utf-8")
    conn.Insert_DB(API_NAME,API_URL,str({"param":REQ_PAR}),str(JSON_DATA),Status,IPADDR,S_TIME,E_TIME)


# ---------- main:
if __name__ == '__main__':
    Second_Hand_Car()
    Find_Car_Goods()
    Check_Tally_Book()
    Check_Etc()
    Wallet()
    Mall()
    MobileApp_First_Page()

    if OK_RESULT:
        OK_CONT = ''
        for i in OK_RESULT:
            OK_CONT = '['+i+']' + OK_CONT
        public.Mail_Alert('%s 巡检正常' % OK_CONT,MYSELF_NAME,'OK')
        #print '%s 巡检正常' % OK_CONT
    if ERR_RESULT:
        ERR_CONT = ''
        for j in ERR_RESULT:
            ERR_CONT = '['+j+']' + ERR_CONT
        public.Sms_Alert('%s 巡检错误' % ERR_CONT,MYSELF_NAME,'CRITICAL')
        #print '%s 巡检错误' % ERR_CONT

