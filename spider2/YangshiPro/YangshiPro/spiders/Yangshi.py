import math
import scrapy
import re
from YangshiPro.items import YangshiproItem
import time
from redis import Redis



class YangshiSpider(scrapy.Spider):
    name = '***'

    start_urls = ['https://search.cctv.com/search.php?qtext=***&sort=relevance&type=web&page=1']

    url_example = 'https://search.cctv.com/search.php?qtext=%s&sort=relevance&type=web&page=%d'

    page_num = 1

    keyword_num = 0

    page_max = 30

    pattern = "(\d+)"

    redis_conn = Redis(host='127.0.0.1',port=6379)

    keywords = [] #关键词列表

    href = '' # 新闻详情页的href

    count = 11564


    def parse(self, response):
        if len(self.keywords) == 0:
            fp = open('keywords.txt', mode='r', encoding='utf-8')
            keyword_list = fp.read().split(',')
            for keyword in keyword_list:
                self.keywords.append(keyword)
            self.keywords = set(self.keywords)
        if self.page_num == 1:
            try:
                news_info = response.xpath("//div[@class='lmdhd']/span/text()")[0].extract()
                news_num = re.findall(pattern=self.pattern,string=news_info)[0]
                pages = math.ceil(int(news_num)/10)
                if pages < 30:
                    self.page_max = pages
            except:
                print("【%s】关键词爬取完毕！" % self.keywords[self.keyword_num])
                self.page_num = 1
                self.page_max = 30
                if self.keyword_num < len(self.keywords):
                    self.keyword_num += 1
                    new_url = format(self.url_example % (self.keywords[self.keyword_num]+'中国', self.page_num))
                    yield scrapy.Request(url=new_url, callback=self.parse, dont_filter=True)

        li_list = response.xpath('//div[@class="outer"]/ul/li')
        for li in li_list:
            try:
                self.href = li.xpath('./div/h3/span/@lanmu1')[0].extract()
                ex = self.redis_conn.sadd('cctv_urls',self.href)
                if ex == 1:
                    time.sleep(2)
                    yield scrapy.Request(url=self.href, callback=self.parse_detail,dont_filter=True)
                    self.href = ''
            except:
                self.redis_conn.srem('cctv_urls',self.href)
                self.href = ''
                continue
        if self.page_num < self.page_max:
            self.page_num += 1
            url = format(self.url_example%(self.keywords[self.keyword_num],self.page_num))
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
        else:
            print("【%s】关键词爬取完毕！" % self.keywords[self.keyword_num])
            self.page_num = 1
            self.page_max = 30
            if self.keyword_num < (len(self.keywords)-1):
                self.keyword_num += 1
                new_url = format(self.url_example % (self.keywords[self.keyword_num], self.page_num))
                yield scrapy.Request(url=new_url, callback=self.parse, dont_filter=True)


    def parse_detail(self,response):
        title = response.xpath('//div[@class="title_area"]/h1/text() | //div[@class="cnt_bd"]/h1/text() | //div[@class="toptitle"]/h1/text() | //div[@class="title"]/text()')[0].extract()
        detail_news_info = ''.join(response.xpath('//div[@class="info1"]/text() | //div[@class="function"]/span/i//text() | //div[@class="info"]/text() | //div[@class="brief"]/span/text()').extract())
        detail_news_origin_title = ''.join(response.xpath('//div[@class="title_area"]/h6/text() | //div[@class="cnt_bd"]/p[@class="o-tit_0505i"]/text()').extract())
        content = ''.join(response.xpath('//div[@class="content_area"]/p//text() | div[@class="text_area"]/p//text()|//div[@class="cont"]/p//text()').extract())


        item = YangshiproItem()
        item['title'] = title
        item['origin_title'] = detail_news_origin_title
        item['info'] = detail_news_info
        item['content'] = content
        item['keyword'] = self.keywords[self.keyword_num]
        item['url'] = self.href
        item['id'] = 'cctv'+str(self.count)

        self.count += 1

        yield item







