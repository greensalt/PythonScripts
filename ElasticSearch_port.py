#!/usr/bin/python2.6
# By xielifeng On 2016-08-30

import os
import json

def discovery():
    PORT=[]
    ElasticSearch = range(9700,9899)

    if os.path.exists('/usr/sbin/ss'):
        PortL = os.popen("ss -lnt4|awk 'NR>1 {print $4}'|awk -F ':' '{print $2}'")
    else:
        PortL = os.popen("netstat -lnt|awk 'NR>2 {print $4}'|awk -F ':' '{print $2}'")

    for port in PortL:
        port = int(port)
        if port in ElasticSearch:
            PORT += [{"{#ELASTICSEARCH}":str(port)}]
    print json.dumps({'data':PORT},sort_keys=True,indent=4)

if __name__ == '__main__':
    discovery()

    
