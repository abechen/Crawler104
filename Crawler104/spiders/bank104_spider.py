# -*- coding: utf-8 -*-
from scrapy import log
from scrapy import Spider
from scrapy.http import Request
from Crawler104.items import Crawler104Item
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup
import datetime
import json


class Bank104SpiderSpider(Spider):
    name = "bank104"
    download_delay = 0.5  # 延遲時間
    allowed_domains = ["www.104.com.tw"]
    start_urls = []

    def __init__(self, category=None, *args, **kwargs):
        super(Bank104SpiderSpider, self).__init__(*args, **kwargs)
        self.filter_string = ['big data', 'hadoop', 'spark', 'data mining', 'data modeling', 'machine learning', 'data analysis','資料分析', '巨量', '大數據', '數據分析']
        self.jobIdList = []

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        for info in soup.select('.j_cont'):
            url = 'http://www.104.com.tw' + info.select('ul[class="summary_tit"] li:nth-of-type(3) a')[0]['href'].split('&')[0]
            yield Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = Crawler104Item()
        soup = BeautifulSoup(response.body, "lxml")
        item['jobId'] = response.url.split('=')[1]
        item['url'] = response.url

        #if item['jobId'] in self.jobIdList:
        #    raise DropItem("Duplicate jobId found: %s" % item['jobId'])
        #else:
        #    self.jobIdList.append(item['jobId'])
            # 抓取看過此工作的人也看以下工作
        #    yield Request('http://www.104.com.tw/job/AjaxSimilar?jobno=%s' % item['jobId'], callback=self.get_similarJobs, dont_filter=True)

        item['crawlDateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['jobName'] = soup.select('.main header div h1')[0].contents[0].strip()
        item['corporation'] = soup.select('.main header div h1 .company a:nth-of-type(1)')[0].get_text(strip=True)
        item['category'] = soup.select('.main section:nth-of-type(1) > .content dl dd:nth-of-type(1)')[0].get_text(strip=True)
        item['conditions'] = soup.select('.main section:nth-of-type(1) > .content dl dd:nth-of-type(2)')[0].get_text(strip=True)
        item['type'] = soup.select('.main section:nth-of-type(1) > .content dl dd:nth-of-type(3)')[0].get_text(strip=True)
        item['address'] = soup.select('.main section:nth-of-type(1) > .content .addr')[0].get_text(strip=True).replace(u"\u5730\u5716\u627e\u5de5\u4f5c", "").lower()
        item['content'] = soup.select('.main section:nth-of-type(1) > .content > p')[0].get_text(strip=True).lower()
        item['experience'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(2)')[0].get_text(strip=True)
        item['educational'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(3)')[0].get_text(strip=True)
        item['department'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(4)')[0].get_text(strip=True)
        item['tools'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(6)')[0].get_text(strip=True)
        item['skills'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(7)')[0].get_text(strip=True)
        item['others'] = soup.select('.main section:nth-of-type(2) .content dl dd:nth-of-type(8)')[0].get_text(strip=True).lower()

        # 需包含特定關鍵字才儲存
        for s in self.filter_string:
            if s in item['content'].encode('utf-8') + '|' + item['others'].encode('utf-8'):
                yield item
                break

        # 抓取看過此工作的人也看以下工作
        yield Request('http://www.104.com.tw/job/AjaxSimilar?jobno=%s' % item['jobId'], callback=self.get_similarJobs, dont_filter=True)

    def get_similarJobs(self, response):
        # json
        jsonresponse = json.loads(response.body_as_unicode())
        for jobs in jsonresponse["data"]["jobs"]:
            jobId = jobs["url"].split('=')[1].split('&')[0]
            if jobId in self.jobIdList:
                raise DropItem("Duplicate jobId found: %s" % jobId)
            else:
                self.jobIdList.append(jobId)
                yield Request('http://www.104.com.tw/' + jobs["url"].split('&')[0], callback=self.parse_detail, dont_filter=True)