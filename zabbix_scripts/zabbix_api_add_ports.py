#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import sys
import urllib2
import argparse

from urllib2 import URLError

reload(sys)
sys.setdefaultencoding('utf-8')

zabbix_url = "http://17.0.4.63/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user = "admin"
zabbix_pass = "zabbix"
auth_code = ""

def user_login():
    data = json.dumps({
                       "jsonrpc": "2.0",
                       "method": "user.login",
                       "params": {
                                  "user": zabbix_user,
                                  "password": zabbix_pass
                                  },
                       "id": 0
                       })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        authID = response['result']
        return authID

auth_id = user_login()

def host_getid(hostIP):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend",
            "filter": {"ip": hostIP}
        },
        "auth": auth_id,
        "id": 1
    })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        hostID = response['result'][0]['hostid']
        hostNAME = response['result'][0]['host']
        return [hostID,hostNAME]

def host_interfaceid(hostIP):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
            "output": "extend",
            "hostids": host_getid(hostIP)[0]
        },
        "auth": auth_id,
        "id": 1
    })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        interfaceID = response['result'][0]['interfaceid']
        return interfaceID

def host_applicationid(hostIP,applicationtype):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "application.get",
        "params": {
            "output": "extend",
            "hostids": host_getid(hostIP)[0],
            "sortfield": "name",
            "filter": {"name": applicationtype}
        },
        "auth": auth_id,
        "id": 1
    })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())

        applicationID = response['result'][0]['applicationid']
        return applicationID

def host_itemtriggercreate(hostIP,applicationtype,itempp):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.create",
        "params": {
            "hostid": host_getid(hostIP)[0],
            "interfaceid": host_interfaceid(hostIP),
            "name": "port $2",
            "type": "7",
            "key_": "net.tcp.port[,%s]" %itempp,
            "value_type": "3",
            "data_type":"0",
            "delay": "120",
            "history": "3",
            "trends": "0",
            "delta": "0",
            "applications": [
                host_applicationid(hostIP, applicationtype)
            ]
        },
        "auth": auth_id,
        "id": 1
    })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        print response

    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "trigger.create",
        "params": {
            "description": "port %s is down on server {HOST.NAME}" %itempp,
            "expression": "{%s:net.tcp.port[,%s].last()}=0" %(host_getid(hostIP)[1],itempp),
            "priority": 4,
            "status": 0
        },
        "auth": auth_id,
        "id": 1
    })
    request = urllib2.Request(zabbix_url, data)
    for key in zabbix_header:
        request.add_header(key, zabbix_header[key])
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        print response

#host_itemtriggercreate(sys.argv[1], sys.argv[2], sys.argv[3])
#host_itemtriggercreate('10.32.40.60','monitor_port','8888')

## Add L.F.Xie On 2017-12-22，支持批量添加：
for PORT in sys.argv[3].split(','):
    host_itemtriggercreate(sys.argv[1], sys.argv[2], PORT)


