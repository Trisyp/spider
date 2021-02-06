from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, DesiredCapabilities, ActionChains
from selenium.webdriver.chrome.options import Options
import os
import time
import random
import requests
from selenium.webdriver.common.keys import Keys

"""
先建立一个作为回调的函数，比如 theforever，在里面对于返回的JSON数据进行处理。
然后在AJAX调用的时候，把建立的回调函数名称加上，比如 &jsonpcallback=theforever
回调函数里面怎么写，取决于返回的JSON和你的业务逻辑。
"""

person_province = "湖北"
person_name = "谢瑶"

proxyHost = "dongtai.xieyaoyun.com"
proxyPort = "33002"

# http://www.xieyaoyun.com:804/  购买的动态代理用户名和密码(防止盗用，下面是假的)
proxyUser = "d086d1deefa83acde"
proxyPass = "b619c89a0dfb86cdf"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
# 代理支持http和https
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


def getDriver(url, phone_num):
    # 构造模拟浏览器
    # chromedriver = r"C:\Users\Administrator\AppData\Local\google\Chrome\Application\chromedriver"
    chromedriver = r"C:\Program Files\Google\Chrome\Application\chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    options = Options()
    options.add_argument('-headless')
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    headers = {
        "Accept": "*/*  ",
        "Host": "vote.wx.news.cn",
        "Referer": "http://h5.wenming.cn/wxtp_wmw/index.html?code=021jgm0w3NVDuV22jj1w32tCCR3jgm0-&state=",
        # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001231) NetType/WIFI Language/zh_CN"
    }
    for key, value in headers.items():
        desired_capabilities["chrome.page.customHeaders.{}".format(key)] = value
    driver = Chrome(desired_capabilities=desired_capabilities, executable_path=chromedriver)
    driver.get(url)  # 打开网址
    html_before = driver.page_source
    xpath_province = '/html/body/div[1]/div/div[1]/div[3]/span[2]'
    time.sleep(1)
    driver.find_element_by_xpath(xpath_province).click()  # 点击省份
    time.sleep(0.5)
    js = "var q=document.getElementsByClassName('scroll-view').scrollTop=100000"
    # driver.execute_script(js)
    driver.execute_script(js)
    driver.execute_script('mobile: scroll', {'direction': 'down'})
    # ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.5)
    xpath_province2 = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/ul'
    province = driver.find_element_by_xpath(xpath_province2)
    all_p = province.find_elements_by_class_name("text")
    # all_p2 = province.find_elements_by_class_name("bar-lite")
    for i in range(len(all_p)):
        if all_p[i].text == person_province:
            all_p[i].click()
            time.sleep(0.5)
            xpath_person = '/html/body/div[1]/div/div[2]/div[3]/div/div'
            xpath_person2 = driver.find_element_by_xpath(xpath_person)  # 点击加入
            name_list = xpath_person2.find_elements_by_class_name("alternative-name")
            join_list = xpath_person2.find_elements_by_class_name("alternative-join")
            for i in range(len(name_list)):
                if name_list[i].text == person_name:
                    join_list[i].click()
                    time.sleep(1)
                    xpath_vote = '/html/body/div[1]/div/div[4]/div[1]/div[2]'
                    driver.find_element_by_xpath(xpath_vote).click()  # 点击点赞
                    time.sleep(1)
                    xpath_shure = '/html/body/div[1]/div/div[5]/div[2]/div[2]/div[4]/span[1]'
                    driver.find_element_by_xpath(xpath_shure).click()  # 点击点赞评议
                    time.sleep(0.5)
                    xpath_number = '/html/body/div[1]/div/div[5]/div[2]/div[2]/div[3]/div/input'
                    driver.find_element_by_xpath(xpath_number).send_keys(str(phone_num))  # 输入手机号
                    time.sleep(1)
                    xpath_check = '/html/body/div[1]/div/div[5]/div[2]/div[2]/div[3]/div/span'
                    driver.find_element_by_xpath(xpath_check).click()  # 点击获取验证码
                    check_num = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                        random.randint(1, 9))
                    time.sleep(0.5)
                    xpath_check_num = '/html/body/div[1]/div/div[5]/div[2]/div[2]/div[3]/input'
                    driver.find_element_by_xpath(xpath_check_num).send_keys(check_num)  # 输入验证码
                    time.sleep(0.5)
                    xpath_sure = '/html/body/div[1]/div/div[5]/div[2]/div[2]/div[4]/span[3]'
                    driver.find_element_by_xpath(xpath_sure).click()  # 点击获取验证码
                    break
            break
    html_after = driver.page_source
    return html_before, html_after


def get_html_info(html):  # 保存网页中间两个表格的内容
    soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
    tag = soup.find_all('div', attrs={'class': {'M-Alternative'}})
    for i in range(len(tag)):
        name = tag[i].find('div', attrs={'class': {'alternative-name'}}).text
        if name == person_name:
            tickets_num = tag[i].find('span', attrs={'class': {'alternative-work'}}).text
            return tickets_num


def get_name_count(phone_num):
    ran_num = random.randint(100, 10000000000)
    url2 = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxec2401ee9a70f3d9&redirect_uri=http%3A%2F%2Fh5.wenming.cn%2Fwxtp_wmw%2Findex.html&response_type=code&scope=snsapi_base&state=&connect_redirect=1#wechat_redirect"  # 首页
    html_before, html_after = getDriver(url2, phone_num)
    count = get_html_info(html_before)
    return count, ran_num


def run():
    num = 1
    phone_num = 15950515345
    while True:
        print(f"---------------------第{num}次投票开始----------------------")
        try:
            count, ran_num = get_name_count(phone_num)
            print("用的手机号：", phone_num)
            print(person_name, "的", count)
            # url = f'http://vote.dx.news.cn/phone/send?phoneNumber={phone_num}&callback={ran_num}'
            # req_header = {
            #     "Host": "vote.dx.news.cn",
            #     "Referer": "http://h5.wenming.cn/",
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            # }
            # response = requests.get(url, req_header)
            # if response.status_code == 200:
            #     time.sleep(0.0001 * random.randint(10, 1000))
            #     print("投票后: ", name, "的", count)
        except Exception as e:
            print(e.__str__())
            continue
        num += 1
        phone_num += 1


if __name__ == '__main__':
    run()
