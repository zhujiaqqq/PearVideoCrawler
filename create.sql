CREATE DATABASE pear;

USE pear;

CREATE TABLE IF NOT EXISTS `pear_video`(
    `id` int unsigned primary key auto_increment,
    `name` varchar(255) not null,
    `author` varchar(40) not null,
    `page_url` varchar(255) not null,
    `video_url` varchar(255),
    `image_url` varchar(255),
    `create_time` varchar(20),
    `content` varchar(255)
);

CREATE TABLE IF NOT EXISTS `pear_author`(
    `id` smallint unsigned primary key auto_increment,
    `author_name` varchar(40) not null,
    `home_url` varchar(255) not null,
    `info` varchar(255)
);