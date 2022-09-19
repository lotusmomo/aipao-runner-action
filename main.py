import requests
import json
import time
import hashlib
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from rich.progress import track

IMEI = os.getenv('IMEI')
API_ROOT = 'http://client3.aipao.me/api/'

# Generate a string contain 10 char
table = ''
for i in range(10):
    table += chr(random.randint(ord('a'), ord('z')))


def sendMsg(content):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    msg['Subject'] = content
    msg['From'] = os.getenv('SMTP_USER')
    send = smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT)'))
    send.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWD'))
    send.sendmail(os.getenv('SMTP_USER'), os.getenv('SMTP_MAILTO'), msg.as_string())


def MD5(str):
    return hashlib.md5(str.encode()).hexdigest()


def encrypt(str):
    result = ''
    for i in str:
        result += table[ord(i) - ord('0')]
    return result


def run():
    if IMEI is None:
        exit("[!]ERROR: No Valid IMEI, Please Check Actions Secrets.")
    if len(IMEI) != 32:
        exit("[!]ERROR: IMEI Format Error.")
    print("[+]INFO: IMEI=" + IMEI)
    tokenHeaders = \
        {
            'version': '2.40',
            'Host': 'client3.aipao.me',
            'Connection': 'Keep-Alive'
        }
    tokenUrl = API_ROOT + 'token/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI
    print("[*]DEBUG: tokenUrl=" + tokenUrl)
    tokenRequests = requests.get(tokenUrl, headers=tokenHeaders)
    tokenJson = json.loads(tokenRequests.content.decode('utf8', 'ignore'))
    state = tokenJson['Success']
    if not state:
        sendMsg('IMEI已过期！')
        exit("[!]ERROR: IMEI Expired.")
    else:
        print("[+]OK: Login Success.")
    token = tokenJson['Data']['Token']
    print("[*]DEBUG: token=" + token)
    userId = str(tokenJson['Data']['UserId'])
    nonce = str(random.randint(100000, 10000000))
    timespan = str(time.time()).replace('.', '')[:13]
    sign = MD5(token + nonce + timespan + userId).upper()
    getSchoolUrl = API_ROOT + token + '/QM_Users/GS'
    print("[*]DEBUG: getSchoolUrl=" + getSchoolUrl)
    schoolHeaders = \
        {
            'nonce': nonce,
            'timespan': timespan,
            'sign': sign,
            'version': '2.14',
            'Accept': None,
            'User-Agent': None,
            'Accept-Encoding': None,
            'Connection': 'Keep-Alive'
        }
    getSchoolRequests = requests.get(getSchoolUrl, headers=schoolHeaders, data={})
    getSchoolJson = json.loads(getSchoolRequests.content.decode('utf8', 'ignore'))
    Lengths = getSchoolJson['Data']['SchoolRun']['Lengths']
    print('[+]INFO:',
          getSchoolJson['Data']['User']['UserID'],
          getSchoolJson['Data']['User']['NickName'],
          getSchoolJson['Data']['User']['UserName'],
          getSchoolJson['Data']['User']['Sex'])
    print('[+]INFO:',
          getSchoolJson['Data']['SchoolRun']['Sex'],
          getSchoolJson['Data']['SchoolRun']['SchoolId'],
          getSchoolJson['Data']['SchoolRun']['SchoolName'],
          getSchoolJson['Data']['SchoolRun']['MinSpeed'],
          getSchoolJson['Data']['SchoolRun']['MaxSpeed'],
          getSchoolJson['Data']['SchoolRun']['Lengths'])
    startRunningUrl = API_ROOT + token + '/QM_Runs/SRS?S1=30.534736&S2=114.367788&S3=' + str(Lengths)
    print("[*]DEBUG: startRunningUrl=" + startRunningUrl)
    startRunningRequests = requests.get(startRunningUrl, headers=schoolHeaders, data={})
    startRunningJson = json.loads(startRunningRequests.content.decode('utf8', 'ignore'))

    # 随机生成跑步数据
    RunTime = str(random.randint(720, 1000))  # 时间（秒）
    RunDist = str(Lengths + random.randint(0, 3))  # 里程
    RunStep = str(random.randint(1300, 1600))  # 步数
    StartT = time.time()
    for i in track(range(int(RunTime))):
        time.sleep(0.1)
        '''
        print("[+]INFO: Current Minutes: %d Running Progress: %.2f%%\r" %
              (i / 60, i * 100.0 / int(RunTime)), end='')
        '''
    print("")
    print("Running Seconds:", time.time() - StartT)
    RunId = startRunningJson['Data']['RunId']

    # 结束跑步
    endUrl = API_ROOT + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
             encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
             '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep) # 拼接url
    print("[*]DEBUG: endUrl=" + endUrl)
    endRequests = requests.get(endUrl, headers=schoolHeaders)
    endJson = json.loads(endRequests.content.decode('utf8', 'ignore'))
    print("----------------------")
    print("Time:", RunTime)
    print("Distance:", RunDist)
    print("Steps:", RunStep)
    print("----------------------")
    if (endJson['Success']):
        sendMsg('跑步成功！')
        print("[+]OK:", endJson['Data'])
    else:
        sendMsg('跑步失败！')
        print("[!]Fail:", endJson['Data'])


if __name__ == '__main__':
    run()