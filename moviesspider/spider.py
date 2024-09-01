import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

#构造出一个叫DataFrame类型的数据
#构造一个字典
# info = {
#     '姓名':['小王','小刘','小张'],
#     '性别':['男','男','女'],
#     '年龄':[22,34,22]
# }
# data = pd.DataFrame(info)
# data.to_excel('./name.xlsx',index=False)

# header={
#     'Referer': 'https://ssr1.scrape.center/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
# }
# response=requests.get('https://p0.meituan.net/movie/283292171619cdfd5b240c8fd093f1eb255670.jpg@464w_644h_1e_1c',headers=header)
#
# print(response.text)
# with open('movie.jpg', 'wb') as f:
#     f.write(response.content)

movie_info = {
    '电影名字':[],
    '类型':[],
    '国家':[],
    '时长':[],
    '上映时间':[],
    '分数':[]
}

header={
    'Referer': 'https://ssr1.scrape.center/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
for page in range(1,11):
    response=requests.get('https://ssr1.scrape.center/page/%d' % page,headers=header)
    # print(response.text)

    soup = BeautifulSoup(response.text,'html.parser')
    result = soup.find_all(name='div',class_='p-h el-col el-col-24 el-col-xs-9 el-col-sm-13 el-col-md-16')

    for t in range(len(result)):

        # print(result[t].h2.string)
        movie_info['电影名字'].append(result[t].h2.string)
        result2 = result[t].find_all(name='button',class_='el-button category el-button--primary el-button--mini')
        movie_type=''
        for i in result2:
            movie_type+=i.span.string + ','
        movie_info['类型'].append(movie_type.rstrip(','))
            # print(i.span.string)


        result3 = result[t].find_all(name='div',class_='m-v-sm info')
        span_list = result3[0].find_all(name='span')
        movie_info['国家'].append(span_list[0].string)
        movie_info['时长'].append(span_list[2].string)
        span_list = result3[1].find_all(name='span')
        if len(span_list) >0:
            movie_info['上映时间'].append(result3[1].span.string)
        else:
            movie_info['上映时间'].append('')

        # for spans in result3:
        #     result4 = spans.find_all(name='span')
        #     for i in result4:
        #         if(i.string != ' / '):
        #             print(i.string)


        result5 = soup.find_all(name='p',class_='score m-t-md m-b-n-sm')
        movie_info['分数'].append(result5[t].string.strip())
        # print(result5[t].string.strip())
        # print('--' * 10)

print(movie_info)
# 检查每个列表的长度
print(len(movie_info['电影名字']))
print(len(movie_info['类型']))
print(len(movie_info['国家']))
print(len(movie_info['时长']))
print(len(movie_info['上映时间']))
print(len(movie_info['分数']))


# info = {
#     '姓名':['小王','小刘','小张'],
#     '性别':['男','男','女'],
#     '年龄':[22,34,22]
# }
data = pd.DataFrame(movie_info)
data.to_excel('./movie.xlsx',index=False)

