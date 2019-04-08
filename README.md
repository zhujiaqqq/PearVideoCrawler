# 梨视频爬虫
## 爬取策略

`https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=0`

**1. 通过视频频道页面进行爬取**
- 方法：GET
- 参数：
   - reqType=5 指定查询视频频道
   - categoryId=6 频道的ID，这里6为美食
   - start=0 从第0个开始查询，默认每次查询12个视频
- 频道Id对照表：

   频道 | 英文 | ID
   :---:|:---:|:---:
   社会 | CHINA | 1
   世界 | WORLD | 2
   财富 | FINFINANCE | 3
   新知 | KNOWLEDGE | 10
   体育 | SPORTS | 9
   生活 | LIFE | 5
   科技 | TECH | 8
   娱乐 | ENTERTAINMENT | 4
   汽车 | AUTO | 31
   美食 | TASTE | 6
   音乐 | MUSIC | 59

**2. 通过作者主页进行爬取**
- 方法：GET
- 参数：
   - reqType=30 指定查询作者主页
   - categoryId=11794266 作者ID，可从数据库中获取
   - start=0 从第0个开始查询，默认每次查询12个视频

**3. 通过标签页面进行爬取**
- 方法：GET
- 参数：
   - reqType=8 指定查询标签页面
   - categoryId=7590 标签ID，可以从数据库获取
   - start=0 从第0个开始查询，默认每次查询12个视频 
   
 ## 数据库
 ### 表一 `pear_video`
    - id
    - name          视频名字
    - author        作者
    - page_url      地址
    - video_url     视频地址
    - image_url     图片地址
    - create_time   创建时间
    - content       简介
    
### 表二 `pear_author`
    - id
    - author_name   作者名字
    - home_url      主页地址
    - info          信息
    
## 点赞接口：

https://www.pearvideo.com/v4/contPraise.msp
formData：contId: 视频ID