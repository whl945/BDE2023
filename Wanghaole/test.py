# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:19:44 2024

@author: whl
"""

#导入相关库
import requests         #获取网页  
from bs4 import BeautifulSoup
import pandas as pd
from snownlp import SnowNLP
# 设置请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}
items = []
for i in range(11,20):
    url=f'https://guba.eastmoney.com/list,zssh000001_{i}.html'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_list = soup.find_all('tr',class_='listitem')#找到所有帖子所在标签
    #print(post_list)
    for post in post_list:
        read_counts = post.find('div',class_='read').text #获取帖子阅读数
        comment_counts = post.find('div',class_='reply').text #获取帖子评论数
        title = post.find('div',class_='title').text #获取帖子标题
        time = post.find('div',class_='update').text #获取更新时间
        item = [read_counts,comment_counts,title,time]
        items.append(item)
        
                
#存储数据
all_data=pd.DataFrame(items,columns=['阅读数','评论数','标题','最后更新'])
all_data.to_excel(r'C:\Users\whl\Desktop\股吧帖子\测试2.xlsx')

#使用SnowNLP计算对每个帖子标题的文字评估情绪得分
def senti(text):
    s=SnowNLP(text)
    return s.sentiments
all_data['情绪']=all_data['标题'].apply(senti)
all_data.to_excel(r'C:\Users\whl\Desktop\股吧帖子\帖子+情感2.xlsx')