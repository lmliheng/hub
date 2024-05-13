### 原理
由于浏览器的同源策略产生的跨域问题，使得CSDN官方URL无法被请求获取展示到前端
使用后端代码GET网页代码，对其进行`数据清洗`，并导入json文件
注意后端程序的`定时任务`以及`日志打印`
前端代码调用本地`json`，也不存在跨域，从而实现需求
### 代码结构
```
├───pyproject/
│   ├───activities.json
│   ├───htmlone.py
│   ├───index.html
│   ├───script.log
```
### 后端
实现HTML转json的数据清洗，以及打印日志到`scripts.log`文件

```python
#作者：小恒不会java
#时间：2024年5月13日
#微信：a13551458597
# -*- coding: utf-8 -*-
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
```
### 定时任务
我服务器系统是linux centos7
**使用cron完成定时运行，并通过python代码日志打印检验运行情况**
比如`scripts.log`
```
[root@iZ7xvavc793m36sybr4bw4Z hub.liheng.work]# cat scripts.log
INFO:root:Script started at 2024-05-13 21:11:36.571745
INFO:root:Script finished at 2024-05-13 21:11:37.311995
[root@iZ7xvavc793m36sybr4bw4Z hub.liheng.work]# 
```
检查cron服务是否正在运行：
```shell
sudo systemctl status cron或者ceond
```
如果cron服务未运行，请使用以下命令启动它：
```shell
sudo systemctl start cron
```
编辑crontab文件
```shell
crontab -e
```
在打开的编辑器中，添加一行以设置定时任务。例如，要每天凌晨1点运行Python脚本，请添加以下行
```shell
0 1 * * * /usr/bin/python /path/to/your/script.py
```
列出当前用户的crontab条目：
```shell
crontab -l
```


### 许可证
本仓库选择`MIT`作为开源许可证
