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
    time.sleep(1)
    return driver


def getHTML(driver):
    html = driver.page_source
    return html


def getText(content): #获取每个table的表名
    result = []
    for j in range(len(content)):
        contentDiv = [content[j].find_all('div')[3], content[j].find_all('div')[6]]
        contentA = content[j].find_all('a')[1]
        contentSpan = content[j].find_all('span')[:10]
        info1 = contentSpan[0].text.replace(" ", "") + "," + contentDiv[0].text.replace(" ",
                                                                                        "") + "," + contentA.text.replace(
            " ", "") + "," + contentDiv[1].text.replace(" ", "")
        for infok in contentSpan[1:]:
            info1 = info1 + "," + infok.text.replace(" ", "")
        if info1:
            result.append(info1)
    return result


def fillUnivlist(html): #保存网页中间两个表格的内容
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('div', attrs={'id': {'KKE_chart_1588337604422'}})
    result2 = getText(tag)
    return tag


def writeUnivlist(result, fpath, num):
    with open(fpath, 'a', encoding='utf-8') as f: #以追加的方式存储内容
        for i in range(num):
            f.write(result[i] + '\n')
        f.close()


if __name__ == '__main__':
    url = "https://quote.cngold.org/gjs/gjhj_xhhj.html"
    driver = getDriver(url)
    html = getHTML(driver)
    result = fillUnivlist(html)
    fpath = 'C:/Users/90539/Desktop/desktop/data.txt'
    # writeUnivlist(result, fpath, len(result))
