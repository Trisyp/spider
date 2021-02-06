import requests
from bs4 import BeautifulSoup
import os
import time
import datetime as dt
from datetime import datetime

week_day_dict = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'}
    r = requests.get(url, headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    r.close()
    return r.text

def getPages(html):
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('table', attrs={'class': {'m-page'}})
    pageTag = tag[0].find_all('ul')
    pageTag1 = pageTag[0].find_all('li')
    pageCount = pageTag1[-3].text
    return int(pageCount)

def getHrefs(html):
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('table', attrs={'class': {'m-tab'}})
    hrefTag = tag[0].find_all('tr')
    del hrefTag[-1]
    del hrefTag[-1]
    hrefs = []
    for i in range(len(hrefTag)):
        hrefTag1 = hrefTag[i].find_all('td')
        hrefTag2 = hrefTag1[-2].find_all('a')
        hrefs.append(hrefTag2[0].get('href'))
    return hrefs


def getTableName(html): #获取每个table的表名
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('div', attrs={'class': {'kj-tit'}})
    tableName = []
    for infoi in tag:
        tableName.append(infoi.text.replace("\n", "").replace(" ", ""))
    return tableName


def fillUnivlist(html): #保存网页中间两个表格的内容
    result = []
    tableNames = getTableName(html)  # 获取表名
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    timeTag = soup.find_all('div', attrs={'class': {'c-time'}})
    numTag = soup.find_all('div', attrs={'class': {'c-num'}})
    ctime = timeTag[0].text[29:39]
    num = numTag[0].text[0:5]
    ctimeweek = datetime.strptime(ctime, "%Y-%m-%d")
    if week_day_dict[ctimeweek.weekday()-1]==num[0:2]:
        oneday = dt.timedelta(days=1)
        ctimeweek1 = ctimeweek-oneday
        ctime1 = ctimeweek1.strftime("%Y-%m-%d")
        dateNumbers = ctime1.replace("-", "") + num[2:5]
    else:
        dateNumbers = ctime + num
    tag = soup.find_all('table', attrs={'class': {'kj-table'}})  # 获取所有表格
    # print(str(tag[0]))
    for i in range(1, 3):
        infoTag = tag[i]
        contentTr = infoTag.find_all('tr')
        for j in range(len(contentTr)):
            if j == 0:
                contentTh = contentTr[j].find_all('th')
                info1 = dateNumbers + "," + tableNames[i]
                for infok in contentTh:
                    info1 = info1 + "," + infok.text.replace(" ", "")
            else:
                contentTd = contentTr[j].find_all('td')
                info1 = dateNumbers + "," + tableNames[i]
                for infok in contentTd:
                    info1 = info1 + "," + infok.text
            result.append(info1)
    return result


def writeUnivlist(result, fpath, num):
    with open(fpath, 'a', encoding='utf-8') as f: #以追加的方式存储内容
        for i in range(num):
            f.write(result[i] + '\n')
        f.close()


def main():
    startDate = input("startDate(格式为yyyy-mm-dd):")
    lastDate = input("lastDate(格式为yyyy-mm-dd):")
    url = "https://dc.simuwang.com/"
    html = getHTML(url)
    pageNumber = getPages(html)
    time.sleep(2)
    hrefs = getHrefs(html)
    count = 1
    for i in range(2, pageNumber+1):
        url = "http://info.sporttery.cn/basketball/match_result.php?page="+str(i)+"&start_date="+startDate+"&end_date="+lastDate
        html = getHTML(url)
        time.sleep(1)
        href = getHrefs(html)
        for hj in href:
            hrefs.append(hj)
        time.sleep(1)
        count += 1
        print("\r当前page进度: {:.2f}%".format(count * 100 / pageNumber), end="")

    # output_href = 'D:/JCWBasketballHrefs.txt'
    # writeUnivlist(hrefs, output_href, len(hrefs))

    count = 0
    output_file = 'D:/JCWBasketball.txt'
    hrefNumber = len(hrefs)
    for i in range(hrefNumber):
        time.sleep(1)
        result = fillUnivlist(getHTML(hrefs[i]))
        time.sleep(1)
        writeUnivlist(result, output_file, len(result))
        count += 1
        print("\r当前href进度: {:.2f}%".format(count * 100 / hrefNumber), end="")

if __name__ == '__main__':
    main()
