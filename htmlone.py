# -*- coding: utf-8 -*-
#作者：小恒不会java
#时间：2024年5月13日
#微信：a13551458597

import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime

logging.basicConfig(filename='script.log', level=logging.INFO)
logging.info('Script started at {}'.format(datetime.now()))

# 获取HTML内容,这种形式是避免get请求的跨域问题
url = 'https://bbs.csdn.net/forums/activity?spm=1035.2022.3001.8781&typeId=745490'
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

activities = []

# 检查做到避免重复活动
posts = soup.find_all('div', {'class': 'content'})
for post in posts:
    activity = {}
    
    # 获取活动名称
    title_element = post.find('div', {'class': 'long-text-title'})
    if title_element:
        activity['name'] = title_element.text.strip()
    
    # 获取活动简介
    desc_element = post.find('div', {'class': 'item-desc'})
    if desc_element:
        activity['description'] = desc_element.text.strip()
    
    # 获取活动链接
    link_element = post.find('a', href=True)
    if link_element:
        activity['link'] = link_element['href']
    
    # 检查活动是否已存在
    if 'link' in activity and not any(existing_activity['link'] == activity['link'] for existing_activity in activities):
        activities.append(activity)

print(activities)

with open('activities.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=4)


logging.info('Script finished at {}'.format(datetime.now()))