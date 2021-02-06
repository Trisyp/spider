# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_html_result(response):  # 保存网页中间两个表格的内容
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
        tag = soup.find('div', attrs={'class': {'main-x rel l'}})
        question_info = tag.find('div', attrs={'class': {'white-x top-x mgb'}})
        person_info = question_info.find('p', attrs={'class': {}})
        person_info2 = person_info.getText(separator=";").split(";")
        q_address = "".join(person_info2[1:3])
        q_time = person_info2[0].strip("咨询时间：")
        q_class = person_info2[3]
        question = question_info.find('h1', attrs={'class': {'subtitle'}}).getText()
        answer_info = tag.find('ul', attrs={'class': {}})
        answer = answer_info.find_all('p', attrs={'class': {'content'}})
        answer_list = [a.getText() for a in answer]
        result = {"question": question, "answer": answer_list, "address": q_address, "time": q_time, "class": q_class}
        return result
    else:
        return {}


if __name__ == '__main__':
    url = 'https://www.lawtime.cn/ask/question_28056946.html'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    result = get_html_result(response)