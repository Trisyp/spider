import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time


def getDriver(url):
    # 构造模拟浏览器
    chromedriver = "C:/Users/90539/AppData/Local/Google/Chrome/Application/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)  # 模拟打开浏览器
    time.sleep(2)
    driver.get(url)  # 打开网址
    # driver.maximize_window() #窗口最大化

    # 模拟登陆
    time.sleep(3)
    driver.find_element_by_xpath('// *[ @ id = "hits"] / div[4] / div / div[1] / div[1] / a').click()  # 点击南理工投票按钮
    # driver.find_element_by_name('tj_login').click() #这样写报错：元素不可见，所以用万能的Xpath
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="challenge-12"]/div[1]/div[4]/div/div[2]/div[1]/div[4]/div/form/button').click()  # 点击喜欢按钮  # 点击登录按钮
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/div/div/div/div/a').click()  # 点击登录按钮
    time.sleep(3)
    driver.find_element_by_name('user[first_name]').clear()  # 先清除输入框内容
    driver.find_element_by_name('user[first_name]').send_keys('huang')  # 输入姓
    time.sleep(3)
    driver.find_element_by_name('user[last_name]').clear()  # 先清除输入框内容
    driver.find_element_by_name('user[last_name]').send_keys('chen')  # 输入名
    time.sleep(3)
    driver.find_element_by_name('user[email]').clear()  # 先清除输入框内容
    driver.find_element_by_name('user[email]').send_keys('1653476146@qq.com')  # 输入邮箱
    time.sleep(3)
    driver.find_element_by_name('user[password]').clear()  # 先清除输入框内容
    driver.find_element_by_name('user[password]').send_keys('1653476146@qq.com')  # 输入邮箱
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="new_user"]/div[6]/div/div/label/span').click()  # 点击接受
    time.sleep(1)
    driver.find_element_by_xpath('// *[ @ id = "new_user"] / div[7] / button / span').click()  # 点击下一步
    time.sleep(1)
    return driver


def getHTML(driver):
    html = driver.page_source
    return html


def fillUnivlist(html): #保存网页中间两个表格的内容
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('div', attrs={'class': {'ranking-table-tbody'}})
    contentEven = tag[0].find_all('div', attrs={'class': {'dc-common-flex aic ranking-table-tbody-tr even'}})
    contentOdd = tag[0].find_all('div', attrs={'class': {'dc-common-flex aic ranking-table-tbody-tr odd '}})
    result1 = getText(contentEven)
    result2 = getText(contentOdd)
    return [*result1, *result2]


if __name__ == '__main__':
    url = "https://techchallenge.thalesgroup.com/en/juries/tYKzclUfUn6H3Dpo7M2LKA/participations/546/vote?hide_voted=false&order=random&scope=all"
    driver = getDriver(url)
    html = getHTML(driver)
        # result = fillUnivlist(html)
        # fpath = 'C:/Users/90539/Desktop/desktop/data.txt'
        # writeUnivlist(result, fpath, len(result))
        # driver.find_element_by_xpath('//*[@id="tab-1-1"]/div/div[2]/div[1]/input').send_keys(f'{i+1}')  # 输入密码
        # time.sleep(1)
        # driver.find_element_by_xpath('//*[@id="tab-1-1"]/div/div[2]/div[1]/a[5]').click()  # 点击登录
        # time.sleep(2)
        # print("第" + str(i + 1) + "页爬取完毕！")