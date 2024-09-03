import requests
from bs4 import BeautifulSoup
import chardet
import re
from ebooklib import epub
from directory import getDirectoryAndLinks
from concurrent.futures import ThreadPoolExecutor, as_completed  # 新增导入多线程模块
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from searchnovle import search_novel

# title_and_author,title_link = search_novel()
# 获取章节目录和链接
linksArray, directoryArray, novelName,request_all_directory_url = getDirectoryAndLinks()

print(linksArray)
print(directoryArray)
print(novelName)
print(request_all_directory_url)

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
header = {
    # 'Referer': 'https://69shuba.cx/book/58911/',
     'Referer': request_all_directory_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}


chapterDataList = []  # 用于存储带有序号的章节数据

# 创建一个带重试机制的 Session,写这个代码是为了解决抓取代码出现443的错误,也就是抓取出现失败的情况
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

# 定义下载章节内容的函数，增加序号参数
def download_chapter(index, oneLink):
    try:
        response = session.get(oneLink, headers=header, proxies=proxies, timeout=10)  # 新增 timeout 参数以防止请求卡住
        detected_encoding = chardet.detect(response.content)['encoding']
        response.encoding = detected_encoding if detected_encoding else 'gbk'  # 设置编码为检测到的编码
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find_all(name='div', class_='txtnav')
        text = soup.get_text(separator='\n', strip=True)  # 用换行符分隔不同段落

        # 清洗开头的数据
        pattern = r".*\d{4}-\d{2}-\d{2}\s*"  # 匹配从开头到日期部分，包括日期本身和其后的空白
        clean_text = re.sub(pattern, '', text, flags=re.DOTALL)

        # 清除结尾的数据
        pattern2 = r"\(本章完\).*"  # 匹配从 (本章完) 开始到文本结束的所有内容
        finel_text = re.sub(pattern2, '', clean_text, flags=re.DOTALL)

        # 获取章节名 和 正文内容
        lines = finel_text.splitlines()

        # 章节名
        chapterName = re.sub(r'（.*?）', '', lines[0]).strip()
        mainContext = '\n'.join(lines[1:])

        # 返回章节数据和序号
        print(f"{chapterName}" + " 已成功抓取")
        return index, chapterName, mainContext
    except Exception as e:
        print(f"抓取失败: {oneLink} - 错误信息: {e}")
        return index, None, None


# 使用多线程并发下载章节内容
with ThreadPoolExecutor(max_workers=50) as executor:  # 使用线程池，max_workers 可根据需求调整
    future_to_url = {executor.submit(download_chapter, i, link): link for i, link in enumerate(linksArray)}  # 提交所有任务
    for future in as_completed(future_to_url):
        index, chapterName, mainContext = future.result()
        if chapterName and mainContext:
            chapterDataList.append((index, chapterName, mainContext))

# 按照原始顺序排序章节数据
chapterDataList.sort(key=lambda x: x[0])

# 创建 EPUB 电子书
book = epub.EpubBook()

# 设置元信息
book.set_title(novelName)
book.set_language('zh')

# 初始化空的章节对象列表，用于生成电子书
epub_chapters = []

# 遍历排序后的章节数据，创建 EPUB 章节
for i, (index, title, content) in enumerate(chapterDataList):
    # 创建每个章节的HTML文件
    chapter = epub.EpubHtml(title=title, file_name=f'chapter_{i + 1}.xhtml', lang='zh')
    # 格式化章节内容，使用 <h1> 标签作为标题，避免在 f-string 中使用反斜杠
    formatted_content = content.replace('\n', '</p><p>')
    chapter.content = f"<h2>{title}</h2><p>{formatted_content}</p>"
    # 将章节添加到电子书中
    book.add_item(chapter)
    epub_chapters.append(chapter)

# 设置目录为章节列表
book.toc = tuple(epub_chapters)

# 添加导航文件
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# 添加 CSS 样式文件
style = 'body { font-family: Arial, sans-serif; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
book.add_item(nav_css)

# 定义书籍的基本结构（封面、目录、样式）
book.spine = ['nav'] + epub_chapters

# 写入并生成 EPUB 文件
epub.write_epub(novelName + '.epub', book, {})
print("EPUB 文件生成完毕！")
