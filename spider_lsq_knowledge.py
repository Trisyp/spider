from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import pandas as pd
import numpy as np
import json
from os import path
import re
# from get_parms import root_dir
# from project_utils.logger import Log


def getDriver(url):
    # 构造模拟浏览器
    chromedriver = r"C:\Program Files\Google\Chrome\Application\chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)  # 模拟打开浏览器
    driver = webdriver.PhantomJS(executable_path="C:\Program Files (x86)\ExtraSoftware\phantomjs-2.1.1-windows\\bin\phantomjs")
    time.sleep(2)
    driver.get(url)  # 打开网址
    # driver.maximize_window() #窗口最大化

    # 模拟登陆
    time.sleep(1)
    # driver.find_element_by_name('tj_login').click() #这样写报错：元素不可见，所以用万能的Xpath
    driver.find_element_by_xpath('//*[@id="username"]').click()  # 点击登录按钮
    time.sleep(1)
    driver.find_element_by_name('username').clear()  # 先清除输入框内容
    driver.find_element_by_name('username').send_keys(u'lsq_xfj02')  # 输入账号
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="password"]').clear()
    # driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(u'Xfj57202371')  # 输入密码
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="submit"]').click()  # 点击登录
    time.sleep(2)
    driver.find_element("type", "text")
    return driver


def page_content_get(driver):

    pass


def run_spider():
    url = "http://49.65.0.116/12345cas/login?service=http%3A%2F%2F49.65.0.116%2Fnjzwfwrx"
    driver = getDriver(url)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="leftNav"]/li[2]/a/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="leftNav"]/li[2]/div/ul/li[1]/a/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="leftNav"]/li[2]/div/ul/li[1]/ul/li/a/span').click()
    # driver.find_element_by_xpath('//*[@id="mini-36"]/span/input').send_keys(100)

    iframe = driver.find_element_by_xpath('//*[@id="tab-content-012800160001"]/iframe')
    driver.switch_to.frame(iframe)
    driver.find_element_by_xpath('//*[@id="mini-36"]/span/input').click()
    driver.find_element_by_xpath('//*[@id="mini-38$3"]/td[2]').click()
    time.sleep(2)
    page_id = 1
    max_pages = 14
    while page_id<max_pages:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tag1 = soup.find_all('li', attrs={'class': 'fui-nav-item top'})
        soup2 = BeautifulSoup(tag1[0], 'html.parser')
        tag1 = soup2.find_all('li', attrs={'class': 'fui-nav-item'})

        table = soup.find('div', attrs={"class","mini-grid-rows-view"})
        case_nos = len(table.find_all('tr'))-2
        start_i = 21
        for x in range(1,case_nos+1):
            driver.find_element_by_xpath(f'//*[@id="{start_i}$cell$3"]/div/a').click()
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            soup.find('div', attrs={"class", "mini-grid-rows-view"})
            driver.find_element_by_xpath('//*[@id="fui-form"]/div[2]/div[1]/h4').text
            start_i = start_i+1

        page_id = page_id+1
    driver.switch_to.default_content()

    pass


if __name__ == "__main__":
    run_spider()
    