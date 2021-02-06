
"""
2017年6月1日15:15:15
读取代理IP网站的API，并获得代理IP
1. 访问西祠代理的API接口
2. 获得数据，并用正则表达式提取关键内容
3. 用列表保存关键内容
"""

import re
import requests


def get_socket_ip(url):
    all_url = []  # 存储IP地址的容器
    r = requests.get(url=url)
    all_url = re.findall(r"\d+\.\d+\.\d+\.\d+\:\d+", r.text)

    with open(r"C:\Users\90539\PycharmProjects\burush_ticket\IP.txt", 'w') as f:
        for i in all_url:
            f.write(i)
            f.write('\n')

    for i in all_url:
        print(i)


def run_get_socket_ip():
    url = "http://api.xicidaili.com/free2016.txt"  # 代理IP的网址
    get_socket_ip(url)


if __name__ == '__main__':
    run_get_socket_ip()
