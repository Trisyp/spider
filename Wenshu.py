#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 裁判文书网爬虫（requests版）
# pip install PyExecJS (需要引用包execjs)

import requests
import execjs
from selenium import webdriver
from time import sleep
import random


class Wenshu:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Referer': 'https://wenshu.court.gov.cn/CallBackController/authorizeCallBack?code=9ff9NU&state=da718fbd-5c1a-49ff-b676-b626d0b60497',
            'Cookie': ''
        }
        self.url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
        self.request = requests.session()
        # 初始化execjs
        node = execjs.get()
        # 加载需要执行的js文件
        self.ctx = node.compile(open('decrypt_content.js', encoding='utf-8').read())
        chrome_options = webdriver.ChromeOptions()
        # 让浏览器不显示自动化测试
        chrome_options.add_argument('disable-infobars')
        self.chrome = webdriver.Chrome(executable_path='C:/Program Files/Google/Chrome/Application/chromedriver.exe', options=chrome_options)

    def send_login(self):
        # 模拟登陆获取到登陆的Cookie
        # self.chrome.get(url='https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login')
        self.chrome.get(url='https://wenshu.court.gov.cn')
        self.chrome.implicitly_wait(10)
        self.chrome.find_element_by_xpath('//*[@id="loginLi"]/a').click()
        self.chrome.implicitly_wait(10)
        # 最大化浏览器
        # self.chrome.maximize_window()
        # 因为登录框在iframe框中，需要先切换到iframe中
        self.chrome.switch_to.frame('contentIframe')
        self.chrome.implicitly_wait(10)
        self.chrome.find_element_by_xpath('//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input').send_keys('13952073885')
        self.chrome.find_element_by_xpath('//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input').send_keys('Adm@1234')
        sleep(random.randint(2, 3))
        self.chrome.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click()
        sleep(random.randint(1, 2))
        xpath_search_base = '//*[@id="_view_1540966814000"]/div/div[1]'
        self.chrome.find_element_by_xpath(xpath_search_base+"/div[2]/input").send_keys('经济犯罪')
        sleep(random.randint(2, 3))
        self.chrome.find_element_by_xpath(xpath_search_base + '/div[3]').click()
        sleep(random.randint(1, 2))
        chookies = self.chrome.get_cookies()
        self.chrome.close()
        # self.chrome.refresh()
        # self.chrome.implicitly_wait(10)
        return chookies

    def decrypt_response(self, ws_content):
        # 解密数据接口返回的加密内容
        # 解密的key
        secret_key = ws_content['secretKey']
        # 加密的数据内容
        result = ws_content['result']
        # 需要执行的方法名，第一个参数加密内容，第二个参数key
        func_name = 'DES3.decrypt("{0}", "{1}")'.format(result, secret_key)
        # 获取解密后的数据内容
        # 此处在windows下执行有报编码错误问题，需要将源码下的subprocess.py文件里的encoding改成utf-8
        return self.ctx.eval(func_name)


wenshu = Wenshu()


def get_headers():
    # 获取登陆后的Cookie
    cookies = wenshu.send_login()
    # 将cookie转换为字符串
    json_cookie = ''
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value']
        json_cookie += name + '=' + value + '; '
    # 退出selenium浏览器自动化
    # Wenshu.chrome.quit()
    print(json_cookie)
    wenshu.headers['Cookie'] = json_cookie
    return wenshu.headers


def get_content(response):
    content = wenshu.decrypt_response(response)
    return content