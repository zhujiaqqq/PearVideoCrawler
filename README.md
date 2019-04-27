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

```mysql-sql
use pear;

create table if not exists `tb_author`
(
  `id`          int           not null primary key auto_increment,
  `author_name` varchar(20)   not null,
  `home_url`   varchar(1000) not null,
  `info`        varchar(1000)
) engine = InnoDB
  auto_increment = 1
  default charset = utf8;

create table if not exists `tb_tag`
(
  `id`              int           not null primary key auto_increment,
  `tag_name`        varchar(20)   not null,
  `tag_id`          varchar(20)   not null,
  `tag_addr`        varchar(1000) not null,
  `tag_video_count` smallint
) engine = InnoDB
  auto_increment = 1
  default charset = utf8;

create table if not exists `tb_video`
(
  `id`           int          not null primary key auto_increment,
  `video_name`   varchar(100)  not null,
  `video_author` varchar(20)   not null,
  `page_url`     varchar(1000) not null,
  `video_url`    varchar(1000) not null,
  `image_url`    varchar(1000) not null,
  `create_time`  datetime      not null,
  `content`      varchar(1000)
) engine = InnoDB
  auto_increment = 1
  default charset = utf8;

delete from tb_video where 1=1;
delete from tb_author where 1=1;
delete from tb_tag where 1=1;
alter table tb_video auto_increment=1;
alter table tb_author auto_increment=1;
alter table tb_tag auto_increment=1;

```
    
## 点赞接口：

https://www.pearvideo.com/v4/contPraise.msp
formData：contId: 视频ID