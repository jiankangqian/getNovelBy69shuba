import requests
from bs4 import BeautifulSoup
import pandas as pd
import chardet


proxies={
'http': 'http://127.0.0.1:7890',
'https': 'http://127.0.0.1:7890'  # https -> http
}


header={
    'Referer': 'https://69shuba.cx/book/56042/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

response = requests.get('https://69shuba.cx/txt/56042/35756202',headers=header,proxies=proxies)
# response.encoding = 'utf-8'
# print(response.text)
# 自动检测编码
encoding = chardet.detect(response.content)['encoding']
response.encoding = encoding

# print(response.text)

soup = BeautifulSoup(response.text,'html.parser')

novel= soup.find(name='div',class_="txtnav")
chapterName = novel.h1.string
print(chapterName)
texts = []
for element in novel.descendants:
        if isinstance(element, str):
            text = element.strip()
            if text:
                texts.append(text)

    # 打印所有文本内容
for text in texts:
    print(text)




