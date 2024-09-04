import requests
from bs4 import BeautifulSoup
import chardet
import re
from ebooklib import epub
from concurrent.futures import ThreadPoolExecutor, as_completed  # 新增导入多线程模块
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib.parse  #URL编码解码模块




def search_novel():
    # 创建一个带重试机制的 Session,写这个代码是为了解决抓取代码出现443的错误，就是解决多线程有的线程因为网络原因抓取失败的问题
    session = requests.Session()

    # 配置重试策略
    retries = Retry(
        total=5,  # 总重试次数
        backoff_factor=0.3,  # 每次重试延迟时间的增长因子
        status_forcelist=[500, 502, 503, 504, 443],  # 遇到这些状态码时触发重试
        allowed_methods=["HEAD", "GET", "OPTIONS"],  # 哪些HTTP方法允许重试
    )

    # 为 session 装载适配器并应用重试策略
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # 设置代理
        proxies = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
        header = {
            # 'Referer': 'https://69shuba.cx/index.html',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            # 'Cookie': 'shuba=11786-11981-22735-5482'
            'sec-ch-ua-platform': '"Windows"',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Host': '69shu.me',
            'Referer': 'https://69shuba.cx/index.html',
        }
        request_url = 'https://69shuba.cx/modules/article/search.php'
        # 设置 Cookie
        cookies = {
            'shuba': '11786-11981-22735-5482',
            'jieqiVisitTime': 'jieqiArticlesearchTime%3D1725364996',
        }

        novel_name = input("请输入要搜索的小说名：")
        # novel_name ='仙府长生'
        encode_novel_name = urllib.parse.quote(novel_name, encoding='gbk')
        form_data = {
            'searchkey': encode_novel_name,
            'submit': 'Search'

        }
        response = session.post(request_url, headers=header,cookies=cookies, proxies=proxies, data=form_data, timeout=10)    # 新增 timeout 参数以防止请求卡住
        detected_encoding = chardet.detect(response.content)['encoding']
        response.encoding = detected_encoding if detected_encoding else 'gbk'  # 设置编码为检测到的编码
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_box = soup.find_all('div', class_='newbox')
        li_box =  div_box[0].find_all('li')
        title_and_author = []
        title_link =[]
        # 遍历所有的 <li> 标签
        t = 0;
        for li in li_box:
            title_tag = li.find('h3').find('a', href=True)
            author_tag = li.find('div', class_='labelbox').find('label')
            # 检查标签是否存在
            if title_tag and author_tag:
                title = title_tag.get_text(strip=True)
                auther= author_tag.get_text(strip=True)
                title_and_author_single = title+' 作者：'+auther
                title_and_author.append(title_and_author_single)
                title_link_single = title_tag['href']
                title_link.append(title_link_single)
                t = t + 1
            else:
                print("标签缺失，跳过该项",t)
        print(title_and_author)
        print(title_link)
        return title_and_author if title_and_author else [],title_link if title_link else []
    except Exception as e:
        print(e)

search_novel()