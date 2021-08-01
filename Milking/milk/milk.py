#run python3 test.py
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))

import requests
import datetime
import re #用于过滤特定文件名
from database import database

# fill in your cookie
# 填入你的 cookie
cookie = ""

def StrOfSize(size):
    '''
    将字节转换成合适的单位
    auth: wangshengke@kedacom.com ；科达柯大侠
    递归实现，精确为最大单位值 + 小数点后三位
    '''
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, round(remainder / 1024, 2), level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ( '{} {}'.format(round(integer+remainder,2), units[level]))

def strOfInt(num):
    num = abs(int(num))
    if num<100000:
        string = "0"*(6-len(str(num)))+str(num)
    elif num<1000000:
        string = str(num)
    else:
        string = str(num%1000000)
    return string

def verify(num, headers):
    string = strOfInt(num)
    url = "https://cowtransfer.com/transfer/verifydownloadcode?code="+string
    # print(url)
    response=requests.get(url, headers=headers)
    response.encoding="utf-8"
    try: #检测有无收到应答
        return response.json()
    except:
        print('Error: No response for verify()')
        return {'valid': False}

def format_time(time_str):
    if '上午' in time_str:
        time_str = time_str.replace('上午','')
    elif '下午' in time_str:
        time_str = time_str.replace('下午','')
        time_strp = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        delta = datetime.timedelta(hours=12)
        time_str = (time_strp+delta).strftime('%Y-%m-%d %H:%M')
    else:
        pass
    
    return time_str

def get_info(guid, headers):
    url = url="https://cowtransfer.com/transfer/files?page=0&guid="+guid
    response=requests.get(url, headers=headers)
    response.encoding="utf-8"
    if not len(response.json()['transferFileDtos'])>0:
        return False
    else:
        return response.json()

def is_trash(fileName):
    blacklist_end=('apk','Appx','bat','cfg','dat','dem','dll','dmg','exe','go','gz','html','info','ipa','ipk','iso','jar','json','key','lock','log','mod','msi','pat','run', 's','sh','sql','tgz','txt','7z')
    blacklist=('男','弟','哥','受','攻','狗','老公','帅哥','金钱爆','金錢爆','抖音','佛','禅','党','openwrt',' com.ss','mmexport')
    blacklist_software=('Vray', 'SketchUp','UGNX','CAD','hydeesoft')
    blacklist_brand=('NIKE','')
    # 排除特定后缀的文件
    if fileName.endswith(blacklist_end):
        return True

    # 排除有特定字的文件
    if any(name in fileName for name in blacklist):
        return True

    if any(name in fileName for name in blacklist_software):
        return True

    if any(name in fileName for name in blacklist_brand):
        return True
    
    # 排除一串数字+下划线开头的（这类一般是抖音视频）
    if re.match('^\d{0,5}_', fileName) != None:
        return True
    
    return False


headers={"accept": "application/json",\
"accept-encoding": "gzip, deflate, br",\
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",\
"cookie":cookie,\
"referer": "https://cowtransfer.com/",\
"sec-fetch-dest": "empty",\
"sec-fetch-mode": "cors",\
"sec-fetch-site": "same-origin",\
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"}

scan_num = 0
def scan(num = None):
    global scan_num
    db = database.MilkDatabase()
    if num != None:
        scan_num = num
    else:
        try:
            scan_num = db.select(start = 0, num = 2, sort = "scanDate", order = 'DESC')[0][0]
        except IndexError:
            print('Error: The database is empty.')
            scan_num = 0
    print("Start to scan from", strOfInt(scan_num))
    while True:
        scan_num += 1
        if scan_num % 100000 == 0:
            db.delete_expired()

        scan_num %= 1000000
        response = verify(num = scan_num, headers = headers)
        if response and response['valid']:
            if not response['transfer']['needPassword'] and response['transfer']['uniqueUrl']:
                try:
                    file_uniqueUrl = response['transfer']['uniqueUrl']
                    file_url="https://cowtransfer.com/s/"+file_uniqueUrl
                except:
                    file_uniqueUrl = ''
                    print(response['transfer'])
                    continue

                
                #url="https://cowtransfer.com/transfer/files?page=0&guid="+response['transfer']['guid']
                #response=requests.get(url, headers=headers)
                file_expireAt = response['transfer']['expireAt']
                file_uploadDate = format_time(response['transfer']['uploadDate'])
                response = get_info(guid = response['transfer']['guid'], headers = headers)

                if not len(response['transferFileDtos'])>0:
                    continue

                file_name=response['transferFileDtos'][0]['fileName']
                file_size=response['transferFileDtos'][0]['sizeInByte']
                file_info = str(scan_num)+'\t'+ file_url+'\t'+file_name+'\t'+StrOfSize(file_size)
                file_datetime = datetime.datetime.strptime(response['transferFileDtos'][0]['createdAt'],'%Y-%m-%d %H:%M:%S')
                file_scanDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file_type = file_name.split(".")[-1] if '.' in file_name else ''

                if is_trash(file_name):
                    print("Find a trash file at", scan_num)
                    continue

                print(scan_num, file_name, StrOfSize(file_size))
                db.replace(values = [scan_num, file_name, file_size, file_uniqueUrl, file_uploadDate, file_expireAt, file_scanDate ,file_type, 0])

    db.close()

if __name__ == "__main__":
    scan(1313)