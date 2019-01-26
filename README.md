# 梨视频爬虫

- 获取频道页面数据
    - 提取视频地址、名称
    - 提取作者信息
    
- 遍历作者主页
    - 提取视频地址、名称
    
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