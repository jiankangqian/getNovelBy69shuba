import requests
from bs4 import BeautifulSoup
import chardet
import re
from ebooklib import epub
from directory import getDirectoryAndLinks
from concurrent.futures import ThreadPoolExecutor, as_completed  # 新增导入多线程模块
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
header = {
    'Referer': 'https://69shuba.cx/index.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

# 创建一个带重试机制的 Session,写这个代码是为了解决抓取代码出现443的错误
session = requests.Session()

# 配置重试策略
retries = Retry(
    total=5,                  # 总重试次数
    backoff_factor=0.3,       # 每次重试延迟时间的增长因子
    status_forcelist=[500, 502, 503, 504,443],  # 遇到这些状态码时触发重试
    allowed_methods=["HEAD", "GET", "OPTIONS"],  # 哪些HTTP方法允许重试
)

# 为 session 装载适配器并应用重试策略
session.mount('https://', HTTPAdapter(max_retries=retries))
request_url = 'https://69shuba.cx/modules/article/search.php'

def search_novel():
    try:
        response = session.get(request_url, headers=header, proxies=proxies, timeout=10)  # 新增 timeout 参数以防止请求卡住
        detected_encoding = chardet.detect(response.content)['encoding']
        response.encoding = detected_encoding if detected_encoding else 'gbk'  # 设置编码为检测到的编码
    except Exception as e:
     print(e)