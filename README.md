# 获全国历史天气爬虫脚本

## 1.数据来源
网址 ：[https://www.tianqi.com/](https://www.tianqi.com/)
![网站图片](doc/1.png)

## 2. 数据库设计
### 2.1 全国城市表
1.表设计

|  字段名称   | 字段类型 | 字段含义|   
|  ----  | ----  | ---- |
| id  | int | 自增主键 |
| province  | varchar | 城市所在省份 中文 |
| province_p  | varchar | 城市所在省份 拼音 |
| municipality  | varchar | 城市所在地级市 中文 |
| municipality_p  | varchar | 城市所在地级市 拼音 |
| area  | varchar | 城市所在区域 中文 |
| area_p  | varchar | 城市所在区域 拼音 |
| city  | varchar | 城市名称 中文 |
| city_p  | varchar | 城市名称 拼音 |
2. mysql ddl
```sql
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `province` varchar(255) DEFAULT NULL COMMENT '省',
  `province_p` varchar(255) DEFAULT NULL COMMENT '省拼音',
  `municipality` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市',
  `municipality_p` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市拼音',
  `area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区',
  `area_p` varchar(255) DEFAULT NULL COMMENT '区拼音',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '城市',
  `city_p` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '城市拼音',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
###2.2 城市天气表

1.表设计

|  字段名称   | 字段类型 | 字段含义|   
|  ----  | ----  | ---- |
| id  | int | 城市id，对应city表中的id |
| date  | varchar | 时间 2020-01-01 |
| temperaturehigh  | varchar | 最高温 |
| temperaturelow  | varchar | 最低温 |
| weather  | varchar | 天气，例：多云  |
| wind  | varchar | 风力风向 |
| city_p  | varchar | 城市名称 拼音 |
2. mysql ddl
```sql
CREATE TABLE `weather` (
  `city_p` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '城市拼音',
  `date` varchar(255) DEFAULT NULL COMMENT '日期',
  `temperaturehigh` varchar(255) DEFAULT NULL COMMENT '最高温',
  `temperaturelow` varchar(255) DEFAULT NULL COMMENT '最低温',
  `weather` varchar(255) DEFAULT NULL COMMENT '天气',
  `wind` varchar(255) DEFAULT NULL COMMENT '风力',
  `id` int(11) DEFAULT NULL COMMENT '城市id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

###2.3 城市天气异常表

1.表设计

|  字段名称   | 字段类型 | 字段含义|   
|  ----  | ----  | ---- |
| year  | int | 异常天气年份 |
| month  | varchar | 异常天气年份 |
| city | varchar | 异常天气城市名称 拼音 |
2. mysql ddl
```sql
CREATE TABLE `errorinfo` (
  `year` int(255) DEFAULT NULL,
  `month` int(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## 3 启动
### 3.1 环境依赖
Python3.7 ,BeautifulSoup,mysql

### 3.2 创建数据库
1. 使用上一节的中建表语句创建3张表，保持表名一直
2. 修改`main.py`中connect的数据库配置
### 3.2 运行
直接运行`main.py`中的main函数

