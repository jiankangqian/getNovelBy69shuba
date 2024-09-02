import requests
from bs4 import BeautifulSoup
import pandas as pd
import chardet
import re
from searchnovle import search_novel

"""获取小说名,小说目录名，小说目录链接，每个链接对应着每章的小说内容,小说名实际已经在sercahnovel中已经抓取到，
所以不必在这个函数里再抓取了，但是我是先写的这个代码，不删除也行"""
title_and_author,title_link = search_novel()
# print(title_and_author)
# print(title_link)
# 显示搜索结果给用户
print("搜索结果：")
for i, name in enumerate(title_and_author):
    print(f"{i + 1}. {name}")

def getDirectoryAndLinks():
    # 设置代理
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    header = {
        'Referer':'https://69shuba.cx/book/58911.htm',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    response = requests.get('https://69shuba.cx/book/58911/', headers=header,proxies=proxies)

    detected_encoding = chardet.detect(response.content)['encoding']
    response.encoding = 'gbk'  # 设置编码为检测到的编码


    soup = BeautifulSoup(response.text,'html.parser')
    result = soup.find_all('div',class_='catalog',id='catalog')
    ulTag = result[0].find_all('ul')
    liTag = ulTag[0].find_all('li')
    # print(liTag)
    # 访问链接目录
    linkArray =[]
    # 所有章节目录
    directoryArray = []

    for li in liTag:
        aTag= li.find('a')
        cleanText = re.sub(r'^\d+\.\s*|\（.*?\）', '', aTag.get_text(strip=True))
        # print(f"链接:{aTag['href']},文本:{cleanText}")
        linkArray.append(aTag['href'])
        directoryArray.append(cleanText)
    linkArray.reverse()
    directoryArray.reverse()

    # 获取小说名
    bread = soup.find('div', class_='bread')
    novelName = bread.find_all('a')[-1].text
    return linkArray,directoryArray,novelName


