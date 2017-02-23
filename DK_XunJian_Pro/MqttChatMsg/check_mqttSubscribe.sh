#!/bin/bash

SPATH=`cd $(dirname $0);pwd`

ps -ef|grep "mqttSubscribe.py"|grep -E -v 'vi|view|more|vim|tail|grep'

if [[ $? != 0 ]];then
    cd $SPATH
    /usr/local/bin/python mqttSubscribe.py > /dev/null 2>&1 
fi
