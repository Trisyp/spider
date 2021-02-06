import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time


def startDriver(): #启动chrome浏览器
    # 构造模拟浏览器
    chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver"  # 驱动所在路径
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)  # 模拟打开浏览器
    time.sleep(2)
    return driver


def getDatenumber(url): #获取主页中的赛事日期和赛事编号
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('table', attrs={"class": {"m-tab"}})
    tag1 = tag[0].find_all('tr')
    dateNumber = []
    for i in range(len(tag1)):
        tag2 = tag1[i].find_all('td')
        try:
            info = tag2[0].text+tag2[1].text #获取标中的内容
        except:
            break
        dateNumber.append(info)
    del dateNumber[-1]
    return dateNumber


def getHTML(driver, url, xpath): #模拟浏览器打开网页，并获得最新窗口中的网页
    driver.get(url)  # 打开网址
    # 模拟点击更多评论
    time.sleep(2)
    driver.find_element_by_xpath(xpath).click()
    time.sleep(3)
    driver.switch_to_window(driver.window_handles[-1]) #跳转到当前窗口
    html = driver.page_source
    return html

def getTableName(html): #获取每个table的表名
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('div', attrs={'class': {'kj-tit'}})
    tableName = []
    for infoi in tag:
        tableName.append(infoi.text.replace("\n", "").replace(" ", ""))
    return tableName


def fillUnivlist(driver, url): #保存网页中间两个表格的内容
    dateNumbers = getDatenumber(url)
    result = []
    count = 0
    for k in range(len(dateNumbers)):
        xpath = "/html/body/div[4]/div[4]/table/tbody/tr["+str(k+1)+"]/td[13]/a"
        html = getHTML(driver, url, xpath)  # 获取HTML
        tableNames = getTableName(html) #获取表名
        soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
        tag = soup.find_all('table', attrs={'class': {'kj-table'}}) #获取所有表格
        # print(str(tag[0]))
        for i in range(1, 3):
            infoTag = tag[i]
            contentTr = infoTag.find_all('tr')
            for j in range(len(contentTr)):
                if j == 0:
                    contentTh = contentTr[j].find_all('th')
                    info1 = dateNumbers[k] + "," + tableNames[i]
                    for infok in contentTh:
                        info1 = info1 + "," + infok.text.replace(" ", "")
                else:
                    contentTd = contentTr[j].find_all('td')
                    info1 = dateNumbers[k] + "," + tableNames[i]
                    for infok in contentTd:
                        info1 = info1 + "," + infok.text
                result.append(info1)
        count += 1
        print("\r当前页进度: {:.2f}%".format(count * 100 / len(dateNumbers)), end="")
    return result


def writeUnivlist(result, fpath, num):
    with open(fpath, 'a', encoding='utf-8') as f: #以追加的方式存储内容
        for i in range(num):
            f.write(result[i] + '\n')
        f.close()


def main():
    for i in range(9):
        driver = startDriver()
        url = "http://info.sporttery.cn/basketball/match_result.php?page="+str(i+1)+"&start_date=2017-11-05&end_date=2017-12-05"  # 要访问的网址
        result = fillUnivlist(driver, url)
        output_file = 'D:/page' + str(i + 1) + '.txt'
        writeUnivlist(result, output_file, len(result))
        driver.close()
        time.sleep(2)
        print("第"+str(i+1)+"页爬取完毕！")

if __name__ == '__main__':
    main()