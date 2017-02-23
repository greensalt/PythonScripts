#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By L.F.Xie On 2017-02-08
# 测试环境部署，暂时没在用

import MySQLdb
import sys

def Insert_DB(api_name,api_url,req_par,res_par,status,ipaddr,s_time,e_time,depend=0):
    return 'ok'
    db = MySQLdb.connect("localhost","xunjian","test:wXJ2017","xunjian" )
    cursor = db.cursor()

    try:
        # 执行sql语句
        cursor.execute('INSERT INTO xunjian.api_xunjian (api_name,api_url,req_par,res_par,status,ipaddr,s_time,e_time,depend) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(api_name,api_url,req_par,res_par,status,ipaddr,s_time,e_time,depend))
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    
    # 关闭数据库连接
    db.close()
