import datetime
import os
from pathlib import Path

import requests
import math
import random
import time
import json

from tqdm import tqdm

from script.spider_wenshu.Wenshu import get_headers, get_content, wenshu

# from base64 import b64encode, b64decode
# from Crypto.Cipher import DES3
BASEDIR = r"C:\Users\90539\PycharmProjects\spide_law_case"

ciphertext = wenshu.ctx.eval("cipher()")
headers_wenshu = get_headers()
session = requests.Session()


class AESCipher:

    def __init__(self, key):
        self.key = key
        self.block_size = 8

    def pad(self, s):
        return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


# 爬取文书列表页
#  数据加密
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


#  爬取文书列表页
def wenshu_list(session, pagenum):
    global headers_wenshu
    url_wenshulist = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'

    data_wenshulist = {
        "pageId": get_pageid(),
        "s8": "03",
        "sortFields": "s50:desc",
        "ciphertext": ciphertext,
        "pageNum": str(pagenum),
        "pageSize": str(5),
        "queryCondition": '[{"key":"s8","value":"03"}]',
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
        "__RequestVerificationToken": get_random(24)
    }

    if pagenum == 1:
        data_wenshulist.pop('pageSize')

    response_wenshulist = session.post(url=url_wenshulist, data=data_wenshulist, headers=headers_wenshu)
    if response_wenshulist.status_code == 200:
        response_json = response_wenshulist.json()
        content = get_content(response_json)
        data = json.loads(content)
        return data["queryResult"]["resultList"]
    else:
        headers_wenshu = get_headers()
        return []


# 爬取文书详情页
def detail_page(docid):
    url_detail = "https://wenshu.court.gov.cn/website/parse/rest.q4w"
    data_detail = {
        "docId": docid,
        "ciphertext": ciphertext,
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
        "__RequestVerificationToken": get_random(24)
    }
    response = session.post(url=url_detail, data=data_detail, headers=headers_wenshu)
    response_json = response.json()
    content = get_content(response_json)
    return json.loads(content)


def get_all_case(input_list, start, end):
    if len(input_list) > 0:
        all_id_list = input_list
    else:
        all_id_list = range(start, end)
    failed_list = {"failed": []}  # 用于存储爬取失败网页id
    title_list_f = f"{BASEDIR}/data/wenshu/title_list.json"
    if Path(title_list_f).exists():
        with open(title_list_f, "r", encoding="utf-8") as f:
            title_list = json.load(f)
    else:
        title_list = {"titles": []}

    doc_id_list_f = f"{BASEDIR}/data/wenshu/doc_id_list.json"
    if Path(doc_id_list_f).exists():
        with open(doc_id_list_f, "r", encoding="utf-8") as f:
            doc_id_list = json.load(f)
    else:
        doc_id_list = {"doc_id": []}

    for i in tqdm(all_id_list):
        j = 1
        try:
            key_list = wenshu_list(session, i)
            time.sleep(0.01 * random.randint(100, 200))
            for key in key_list:
                docid = key["rowkey"]
                if docid in doc_id_list["doc_id"]:
                    print("文档id重复")
                    continue
                doc_id_list["doc_id"].append(docid)
                with open(f"{BASEDIR}/data/wenshu/doc_id_list.json", "w", encoding="utf-8") as f:
                    json.dump(doc_id_list, f, ensure_ascii=False)
                doc_json = detail_page(docid)
                file_title = doc_json['s1']
                if file_title in title_list["titles"]:
                    print("标题重复")
                    continue
                filename = f"{i}-{j}_{file_title.strip()[:51]}.json"
                filename = filename.replace("\"", "“")
                os.makedirs(f"{BASEDIR}/data/wenshu", exist_ok=True)
                with open(f"{BASEDIR}/data/wenshu/{filename}", "w", encoding="utf-8") as f:
                    json.dump(doc_json, f, ensure_ascii=False)
                print(f"页面{i}-{j}爬取完成。", filename)
                title_list["titles"].append(file_title)
                with open(f"{BASEDIR}/data/wenshu/title_list.json", "w", encoding="utf-8") as f:
                    json.dump(title_list, f, ensure_ascii=False)
                j += 1
                time.sleep(0.01 * random.randint(200, 300))
        except Exception as e:
            print("error", e)
            print(f"页面{i}-{j}爬取失败！！！")
            time.sleep(5)  # 先暂停10秒再爬
            failed_list["failed"].append(i)
        with open(f"{BASEDIR}/data/wenshu/failed_list.json", "w", encoding="utf-8") as f:
            json.dump(failed_list, f, ensure_ascii=False)
    return failed_list, title_list, doc_id_list


if __name__ == "__main__":
    input_list = []
    failed_list, title_list, doc_id_list = get_all_case(input_list, 1, 10000)
