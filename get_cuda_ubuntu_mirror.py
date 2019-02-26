#!/usr/local/py3env/bin/python3
#-*- coding: utf-8 -*-
# author: 谢李锋
# On 2019-02-14

import requests
import re
import subprocess
import datetime

def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    retcode = subprocess.call(cmd, shell=True)
    return retcode

def getNowTime():
    now_time = datetime.datetime.now()
    format_now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")

    return format_now_time

def writeLog(log_content):
    now_time = getNowTime()
    day_time = now_time.split()[0].replace("-", "")
    log_file = '/dev/shm/%s_cuda_ubuntu_download.log' % day_time

    with open(log_file, 'a+', encoding='utf-8') as f:
        f.write('%s\n' % log_content)

def downRepo(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:64.0) Gecko/20100101 Firefox/64.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    r = requests.get(url, headers=headers)
    pattern = '<a href=\'(.+)\'>'

    links = re.findall(pattern, r.text)
    links.remove('..')

    if links:
        for link in links:
            sh_cmd = 'wget %s/%s -t 2 -N -r -c -np -nH -R index* --cut-dirs 3 --restrict-file-names=nocontrol -e robots=off -P /data/didiyum/mirrors/public/cuda/ubuntu/' % (url, link)
            if bash(sh_cmd) == 0:
                log = "%s [ OK ] <%s>" % (getNowTime(), sh_cmd)
                writeLog(log)
            else:
                log = "%s [ ERROR ] <%s>" % (getNowTime(), sh_cmd)
                writeLog(log)

def readLocalFile(check_file):
    with open(check_file, 'r', encoding='utf-8') as f:
        md5_value = f.readline().strip()
    return md5_value


def checkMd5(url, path):
    md5_file_name = 'Packages.gz.md5'
    local_md5_file = '%s/%s' % (path, md5_file_name)
    remote_md5_file = "%s/%s" % (url, md5_file_name)

    if local_md5_file:
        local_md5_value = readLocalFile(local_md5_file).split()[0]

    try:
        r = requests.get(remote_md5_file)
        r_md5_value = r.text.split()[0]

        if local_md5_value == r_md5_value:
            log = "%s [ OK ] local == remote, <%s> nothing." % (getNowTime(), remote_md5_file)
            writeLog(log)
        else:
            log = "%s [ Warning ] local(%s) != remote(%s), <%s> need update." % (getNowTime(),local_md5_value,r_md5_value, remote_md5_file)
            writeLog(log)
            downRepo(url)
    except:
        err_log = "%s [ ERROR ] requests.get[%s] failed." % (getNowTime(), remote_md5_file)
        writeLog(err_log)



if __name__ == '__main__':
    u1404_url = 'https://developer.download.nvidia.cn/compute/cuda/repos/ubuntu1404/x86_64'
    u1404_local_path = '/data/mirrors/public/cuda/ubuntu/ubuntu1404/x86_64/'

    u1604_url = 'https://developer.download.nvidia.cn/compute/cuda/repos/ubuntu1604/x86_64'
    u1604_local_path = '/data/mirrors/public/cuda/ubuntu/ubuntu1604/x86_64/'

    checkMd5(u1404_url, u1404_local_path)
    checkMd5(u1604_url, u1604_local_path)
