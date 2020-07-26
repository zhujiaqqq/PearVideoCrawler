USE exapp;
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