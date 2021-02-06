#!/usr/bin/python
# coding=utf-8
import time
import random
import requests


def run():
    while True:
        url = 'https://s.wcd.im/ajax/log_h.jsp?cmd=dog&dogId=2000496&dogSrc=2&aid=15897763&flyerAid=2781483&flyerId=283'
        url2 = "https://s.wcd.im/index.jsp?id=2ks9bZ8r&flyerAid=2ks9b&loading=1&sid=9epe&chl=&isRemVersion=true"
        try:
            req_header = {
                "Host": "s.wcd.im",
                "Referer": "https://s.wcd.im/index.jsp?id=2ks9bZ8r&flyerAid=2ks9b&loading=1&sid=9epe&chl=&isRemVersion=true",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
            response = requests.get(url, req_header)
            if response.status_code == 200:
                response2 = requests.get(url2, req_header)
                html = str(response2.content, "utf-8")
                print(html[html.find("全城接力"):(html.find("九江代言的人") + 6)])
        except Exception as e:
            print(e.__str__())
            continue
        time.sleep(2.5*random.randint(2, 10))


if __name__ == '__main__':
    run()
