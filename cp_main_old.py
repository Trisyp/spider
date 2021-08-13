import requests
import math
import random
import time
import json
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad, pad


# 爬取文书列表页
## 数据加密
def get_pageid():
    return ''.join([format(math.floor(random.random() * 16), 'x') for i in range(32)])


def get_random(size):
    str = ''
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
           'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(size):
        str += arr[round((random.random() * (len(arr) - 1)))]
    return str


def strTobinary(str):
    result = []
    ls = list(str)
    return ' '.join(list(map(lambda x: format(ord(x), 'b'), ls)))


def get_ciphertext():
    timestamp = time.time()
    timestamp_str = str(round(timestamp * 1000))
    salt = get_random(24)
    iv = time.strftime('%Y%m%d', time.localtime(timestamp))
    crypt = DES3.new(key=salt, mode=DES3.MODE_CBC, iv=iv.encode())
    text = pad(timestamp_str.encode(), DES3.block_size)
    ciphertext = crypt.encrypt(text)
    enc = base64.b64encode(ciphertext).decode("utf-8")
    return strTobinary(salt + iv + enc)


## 结果解密
def get_result(result, secretKey):
    timestamp = time.time()
    iv = time.strftime('%Y%m%d', time.localtime(timestamp))
    crypt = DES3.new(key=secretKey.encode(), mode=DES3.MODE_CBC, iv=iv.encode())
    decrypted_data = crypt.decrypt(base64.b64decode(result))
    plain_text = unpad(decrypted_data, DES3.block_size).decode()
    return plain_text


## 爬取文书列表页
def wenshu_list(session, pagenum, headers_wenshu):
    url_wenshulist = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'

    data_wenshulist = {
        "pageId": get_pageid(),
        "s8": "03",
        "sortFields": "s50:desc",
        "ciphertext": get_ciphertext(),
        "pageNum": str(pagenum),
        "pageSize": str(5),
        "queryCondition": '[{"key":"s8","value":"03"}]',
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
        "__RequestVerificationToken": get_random(24)
    }

    if pagenum == 1:
        data_wenshulist.pop('pageSize')

    response_wenshulist = session.post(url=url_wenshulist, data=data_wenshulist, headers=headers_wenshu)
    secretKey = response_wenshulist.json()['secretKey']
    result = response_wenshulist.json()["result"]
    data = json.loads(get_result(result, secretKey))

    return data["queryResult"]["resultList"]


# 爬取文书详情页
def detail_page(docid, headers_wenshu):
    url_detail = "https://wenshu.court.gov.cn/website/parse/rest.q4w"

    data_detail = {
        "docId": docid,
        "ciphertext": get_ciphertext(),
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
        "__RequestVerificationToken": get_random(24)
    }
    response = session.post(url=url_detail, data=data_detail, headers=headers_wenshu)
    json_value = response.json()
    secretKey = json_value["secretKey"]
    result = json_value["result"]
    return json.loads(get_result(result, secretKey))


if __name__ == "__main__":
    session = requests.Session()
    # cookies = get_cookies(session)
    # session.cookies = cookies
    headers_wenshu = {
        'Connection': 'keep-alive',
        'Cookie': 'SESSION=881ab4bb-bf41-447b-8dda-9bbc4ee38f36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
    }

    i = 1
    j = 1
    detail_result_list = []
    try:
        while True:
            key_list = wenshu_list(session, i, headers_wenshu)
            time.sleep(0.01 * random.randint(300, 500))
            for key in key_list:
                docid = key["rowkey"]
                detail_result_list.append(detail_page(docid, headers_wenshu))
                if len(detail_result_list) >= 500:
                    with open('./data/%s.json' % j, 'w') as file:
                        json.dump(detail_result_list, file, ensure_ascii=False)
                    j += 1
                    detail_result_list = []
                time.sleep(0.01 * random.randint(200, 500))
            print(f"第{i}页文书爬取完成")
            time.sleep(0.01 * random.randint(200, 500))
            i += 1
    except Exception as e:
        print(e.__str__())
        with open('./log/except.txt', 'w') as file:
            file.write(f"第{i}页文书爬取完成 \n" + e.__str__())
        with open('./data/%s.json' % j, 'w') as file:
            json.dump(detail_result_list, file, ensure_ascii=False)
