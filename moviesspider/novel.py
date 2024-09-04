import requests
from bs4 import BeautifulSoup
import chardet
import re
from ebooklib import epub
from directory import getDirectoryAndLinks
from concurrent.futures import ThreadPoolExecutor,as_completed


# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
header = {
    'Referer':'https://69shuba.cx/book/58911/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}
linksArray,directoryArray,novelName = getDirectoryAndLinks()

print(linksArray)
print(directoryArray)
print(novelName)


chapterNameList = []
mainContextList = []
# 定义下载章节内容的函数
def downloadChapter(oneLink):
    try:
        response = requests.get(oneLink, headers=header, proxies=proxies, timeout=10)
        # 检测编码
        detected_encoding = chardet.detect(response.content)['encoding']
        response.encoding = detected_encoding if detected_encoding else 'gbk'
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

        # 返回章节名和内容
        print(f"{chapterName}" + " 已成功抓取")
        return chapterName, mainContext
    except Exception as e:
        print(f"抓取失败: {oneLink} - 错误信息: {e}")
        return None, None

# for oneLink in linksArray:
#     response = requests.get(oneLink, headers=header, proxies=proxies)
#
#     # 检测编码
#     detected_encoding = chardet.detect(response.content)['encoding']
#     response.encoding = 'gbk'  # 设置编码为检测到的编码
#     #获取每个章节的内容,包括章节名,正文
#     soup = BeautifulSoup(response.text, 'html.parser')
#     result = soup.find_all(name='div', class_='txtnav')
#     # print(result)
#     text = soup.get_text(separator='\n', strip=True)  # 用换行符分隔不同段落
#     # print(text)
#     # 清洗开头的数据
#     pattern = r".*\d{4}-\d{2}-\d{2}\s*"  # 匹配从开头到日期部分，包括日期本身和其后的空白
#     clean_text = re.sub(pattern, '', text, flags=re.DOTALL)
#     # print(clean_text)
#     # 清楚结尾的数据
#     pattern2 = r"\(本章完\).*"  # 匹配从 (本章完) 开始到文本结束的所有内容
#     finel_text = re.sub(pattern2, '', clean_text, flags=re.DOTALL)  # 用空字符串替换匹配的部分
#
#     # 获取章节名 和 正文内容
#     # 分割文本为多行
#     lines = finel_text.splitlines()
#
#     # 章节名
#     chapterName = re.sub(r'（.*?）', '', finel_text.splitlines()[0]).strip()
#     # chapterName = finel_text.splitlines()[0]
#     chapterNameList.append(chapterName)
#
#     # 去除第一行后的内容,正文
#     mainContext = '\n'.join(lines[1:])
#     mainContextList.append(mainContext)
#     print(f"{chapterName}"+"已成功抓取")

# 使用多线程并发下载章节内容
# 使用线程池，max_workers 可根据需求调整
with ThreadPoolExecutor(max_workers=5) as executor:
    futureToUrl = {executor.submit(downloadChapter,link):link for link in linksArray} # 提交所有任务
    for future in as_completed(futureToUrl):
        chapterName, mainContext = future.result()
        if chapterName and mainContext:
            chapterNameList.append(chapterName)
            mainContextList.append(mainContext)



# 创建 EPUB 电子书
book = epub.EpubBook()

# 设置元信息
book.set_title(novelName)
book.set_language('zh')
# book.add_author('文抄公')




# 初始化空的章节对象列表，用于生成电子书
epub_chapters = []


# 遍历章节名和正文内容，创建 EPUB 章节
for i, (title, content) in enumerate(zip(chapterNameList, mainContextList)):
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
epub.write_epub(novelName+'.epub', book, {})
print("EPUB 文件生成完毕！")





