# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class Crawler104Item(scrapy.Item):
    # define the fields for your item here like:
    jobId = Field()             # 職務ID
    crawlDateTime = Field()     # 爬蟲抓取時間
    url = Field()               # 職缺網址
    jobName = Field()           # 職務名稱
    corporation = Field()       # 公司名稱
    category = Field()          # 職務類別
    conditions = Field()        # 工作待遇
    type = Field()              # 工作性質
    address = Field()           # 公司地址
    content = Field()           # 工作內容
    experience = Field()        # 工作經歷
    educational = Field()       # 學歷要求
    department = Field()        # 科系要求
    tools = Field()             # 擅長工具
    skills = Field()            # 工作技能
    others = Field()            # 其他條件
