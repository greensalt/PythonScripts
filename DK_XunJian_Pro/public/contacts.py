#!/usr/bin/env python
# -*- coding: utf-8 -*-
# EMail

# Alert Contacts:

def Contacts():
    DK_Users = ['yun@test.com',
                 'waxi@test.com',
                 'diwe@test.com'
                ]
    OPS_Users = ['lin@test.com',
                 'mng@test.com',
                 'tor@test.com'
                ]
    S_OPS_Users = ['eg@test.com']
    Mail_User = DK_Users+OPS_Users+S_OPS_Users
    #Mail_User = ['xi@test.com']

    
    # 去重:
    Receiver_User = list(set(Mail_User))

    return Receiver_User
