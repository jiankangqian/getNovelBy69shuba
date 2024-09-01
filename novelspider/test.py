import requests
from bs4 import BeautifulSoup
import chardet
import re


# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
header = {
    'Referer': 'https://69shuba.cx/book/58911.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}
response = requests.get('https://69shuba.cx/book/58911/', headers=header, proxies=proxies)

detected_encoding = chardet.detect(response.content)['encoding']
response.encoding = 'gbk'  # 设置编码为检测到的编码

soup = BeautifulSoup(response.text, 'html.parser')
result = soup.find_all('div', class_='catalog', id='catalog')
ulTag = result[0].find_all('ul')
liTag = ulTag[0].find_all('li')
# print(liTag)
# 访问链接目录
linkArray = []
# 所有章节目录
directoryArray = []

for li in liTag:
    aTag = li.find('a')
    cleanText = re.sub(r'^\d+\.\s*|\（.*?\）', '', aTag.get_text(strip=True))
    # print(f"链接:{aTag['href']},文本:{cleanText}")
    linkArray.append(aTag['href'])
    directoryArray.append(cleanText)
linkArray.reverse()
directoryArray.reverse()

#获取小说名
bread = soup.find('div', class_='bread')
auther = bread.find_all('a')[-1].text
# print(bread)
# print( bread.find_all('a'))
print(auther)