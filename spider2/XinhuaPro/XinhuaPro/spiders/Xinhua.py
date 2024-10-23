import json
from redis import Redis
from XinhuaPro.items import XinhuaproItem
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class XinhuaSpider(scrapy.Spider):
    name = '***'

    count = 300000

    keyword_num = 0

    with open('keywords.txt', 'r', encoding='utf-8') as fp:
        keywords = fp.read().split(',')


    url_pattern = 'http://so.news.cn/getNews?keyword=%s&curPage=%d&sortField=0&searchFields=0&lang=cn'

    redis_conn = Redis(host='127.0.0.1', port=6379)

    def start_requests(self):
        yield scrapy.Request(url=self.url_pattern % (self.keywords[0], 1), callback=self.first_parse, dont_filter=True,
                             errback=self.errback_httpbin)

    def first_parse(self, response):
        data = json.loads(response.text)
        if data['code'] == 200:
            result_list = data['content']['results']
            if result_list is not None:
                pages = int(data['content']['pageCount'])
                for result in result_list:
                    url = result['url']
                    self.count += 1
                    news_data = {
                        'time': result['pubtime'],
                        'id': 'xh' + str(self.count),
                        'url': url,
                        'keyword': data['content']['keyword']
                    }
                    try:
                        ex = self.redis_conn.sadd('xh_urls', url)
                        if ex == 1:
                            yield scrapy.Request(url=url, callback=self.detail_parse, cb_kwargs=dict(data=news_data),
                                                 dont_filter=True, errback=self.errback_httpbin)
                    except Exception as e:
                        print(e)
                        continue

                for i in range(2, pages + 1):
                    print('------------' + self.keywords[self.keyword_num] + '第%d页' % i + '-------------')
                    new_url = self.url_pattern % (self.keywords[self.keyword_num], i)
                    yield scrapy.Request(url=new_url, callback=self.other_parse, dont_filter=True,
                                         errback=self.errback_httpbin)

            print('【%s】关键词爬取完毕！' % self.keywords[self.keyword_num])
            fp2 = open('log.txt', 'a', encoding='utf-8')
            fp2.write('\n【%s】关键词爬取完毕！' % self.keywords[self.keyword_num])
            fp2.close()
            if self.keyword_num < len(self.keywords):
                self.keyword_num += 1
                yield scrapy.Request(url=self.url_pattern % (self.keywords[self.keyword_num], 1),
                                     callback=self.first_parse, dont_filter=True, errback=self.errback_httpbin)

    def other_parse(self, response):
        data = json.loads(response.text)
        if data['code'] == 200:
            result_list = data['content']['results']
            if result_list is not None:
                for result in result_list:
                    url = result['url']
                    self.count += 1
                    news_data = {
                        'time': result['pubtime'],
                        'id': 'xh' + str(self.count),
                        'url': url,
                        'keyword': data['content']['keyword']
                    }
                    try:
                        ex = self.redis_conn.sadd('xh_urls', url)
                        if ex == 1:
                            yield scrapy.Request(url=url, callback=self.detail_parse, cb_kwargs=dict(data=news_data),
                                                 dont_filter=True, errback=self.errback_httpbin)
                    except Exception as e:
                        print(e)
                        continue

    def detail_parse(self, response, data):
        title = ''.join(response.xpath("//h1//text()").extract())
        content = ''.join(response.xpath('//p//text() ').extract())
        item = XinhuaproItem()
        item['title'] = title
        item['info'] = data['time']
        item['content'] = content
        item['keyword'] = data['keyword']
        item['url'] = data['url']
        item['id'] = data['id']
        yield item

    # 从scrapy官方文档中摘抄而来，当爬取报错之时会运行这个函数
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
