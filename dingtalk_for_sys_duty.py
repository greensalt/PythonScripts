#-*-coding:utf-8-*-
# By Lion.Xie On 2019-01-18

import requests
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def timeToTimeStamp(string):
    # string = '2019-01-11 00:00:00'
    time_array = time.strptime(string, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))

    return time_stamp

# 从值班系统抓取当前值班信息
def getDutyInfo():
    cmdb_url = 'http://zhiban.test.com/getScheduledDuty'
    data = {'username':'l0GP7Kntz='}
    headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:64.0) Gecko/20100101 Firefox/64.0',
    }

    r = requests.post(cmdb_url,data=data,headers=headers,timeout=(3,30))
    r.encoding = 'utf-8'
    rs = json.loads(r.text, encoding='utf-8')
    source_data = rs['aaData']

    duty_dict = {}
    now_time = int(time.time())

    for n in range(0,len(source_data)):
        if source_data[n]['dutyTypeName'] == u'系统值班':
            #start_time = timeToTimeStamp(source_data[n]['dutyStartTime'])
            #end_time = timeToTimeStamp(source_data[n]['dutyEndTime'])
            end_time = source_data[n]['dutyEndTime'].split(' ')[0]
            start_time = source_data[n]['dutyStartTime'].split(' ')[0]
            start_time = timeToTimeStamp("%s 17:00:00" % start_time)
            end_time = timeToTimeStamp("%s 16:59:59" % end_time)


            if now_time > start_time and now_time < end_time:
                duty_dict['dutyMaster'] = source_data[n]['dutyMaster']
                duty_dict['dutyBackup'] = source_data[n]['dutyBackup']

    if duty_dict:
        return duty_dict
    else:
        return False

def sendMsgToDingDingForText():
    # 测试群
    #DingDing_URL = 'https://oapi.dingtalk.com/robot/send?access_token=f01ae9b00f08dec3f961b'
    # 线上群
    DingDing_URL = 'https://oapi.dingtalk.com/robot/send?access_token=25cee6f8b4f15d9b05419e'
    duty_info = getDutyInfo()
    duty_master = duty_info['dutyMaster']
    duty_backup = duty_info['dutyBackup']

    ARG = {
    "feedCard": {
        "links": [
            {
                "title": "今日系统部值班安排",
                "messageURL": "",
                "picURL": "https://timgsa.baidu.com/timg?image&quality=80&size=b10000_10000&sec=1555664924&di=d8f7c3b772891e27f568de420f1facd3&src=http://00.imgmini.eastday.com/mobile/20171228/20171228175020_da92ab0a812b6c76fc1edea78a2d3f5a_1.jpeg"
            },
            {
                "title": "【主】%s" % duty_master,
                "messageURL": "",
                "picURL": "https://timgsa.baidu.com/timg?image&quality=80&size=b10000_10000&sec=1555664924&di=7985699538910abf262b57d7d7875356&src=http://img.zcool.cn/community/015c2c55572fb40000009af0e9caae.jpg"
            },
            {
                "title": "【备】%s" % duty_backup,
                "messageURL": "",
                "picURL": "https://timgsa.baidu.com/timg?image&quality=80&size=b10000_10000&sec=1555664924&di=34ed0b550ec9476898cf82596f64e41f&src=http://n.sinaimg.cn/sports/2_img/upload/17ef47c9/708/w960h548/20180602/Wh-q-hcikcew9066212.jpg"
            }
        ]
    },
    "msgtype": "feedCard"
}
    #ARG = {
    #    "msgtype": "text",
    #    "text": {
    #        "content": "测试"
    #    },
    #    #"at": {
    #    #    "atMobiles": [
    #    #        "1877xxxxxxx"
    #    #    ],
    #    #    "isAtAll": 'false'
    #    #}
    #}

    headers = {'user-agent': 'application/json'}
    try:
        r = requests.post(DingDing_URL, json=ARG, headers=headers, timeout=(3,60))
    except:
        print("Send MSG is fail!")
    print(r.text)

if __name__ == '__main__':
    sendMsgToDingDingForText()
