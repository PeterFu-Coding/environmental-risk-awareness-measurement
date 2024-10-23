import json
import random
import time
import urllib3
from redis import Redis
import requests
from GMDetail import get_detail_news



keywords = []
# id 计数
count = 0

fp = open('keywords.txt', 'r', encoding='utf-8')

keywords = fp.read().split(',')
keywords = list(set(keywords))

keyword_num = 0

# 连接redis
redis_conn = Redis(host='127.0.0.1', port=6379)

# 爬虫pattern
# 其中q = %s 表示关键词, c = %s 表示素材库，包括光明网新闻（n）、光明日报(g)、文摘报(wz)和中华读书报(ds), cp = %d表示第几页
url_pattern = 'https://zhonghua.cloud.gmw.cn/service/search.do?q=%s&c=%s&cp=%d'

# 编辑请求头
headers = {
    "user-agent": '***'
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sources = ['g', 'wz', 'ds']
for source in sources:
    keyword_num = 0
    while keyword_num < len(keywords):
        fp2 = open('***.txt', 'a', encoding='utf-8')
        keyword = keywords[keyword_num]
        page_num = 1
        content_sum = 0
        if page_num == 1:
            url = url_pattern % (keyword, source, page_num)
            try:
                rand = random.randint(0, 5)
                time.sleep(rand)
                response = requests.get(url=url, headers=headers, verify=False)
                # print(response.raw._connection.sock.getpeername())
                response.encoding = response.apparent_encoding
                response_text = str(response.text).lstrip('null(').rstrip(')')
                response_json = json.loads(response_text)
                if not response_json['isBlock']:
                    # 获取每个详情页的url
                    url_list = response_json['result']['list']
                    for list in url_list:
                        detail_url = list['url']
                        info = list['master'] + list['pubtime']
                        try:
                            ex = redis_conn.sadd('gm_urls', detail_url)
                            if ex == 1:
                                get_detail_news(url=detail_url, keyword=keyword, id='gm' + str(count), info=info)
                                count += 1
                            response.close()
                        except Exception as e:
                            print('第一页：' + detail_url + ',' + str(e))
                            continue

                    content_sum = response_json['page']['totalCount']
                    # 进一法
                    page_num = int(round(content_sum / 10 + 0.4, 0))
                else:
                    print('被封了！')
                    time.sleep(600)
            except Exception as e:
                print('第一页：' + url + ',' + str(e))
                continue

        for i in range(2, page_num + 1):
            url = url_pattern % (keyword, source, i)
            try:
                rand = random.randint(0, 5)
                time.sleep(rand)
                response = requests.get(url=url, headers=headers, verify=False)
                response.encoding = response.apparent_encoding
                response_text = str(response.text).lstrip('null(').rstrip(')')
                response_json = json.loads(response_text)

                if not response_json['isBlock']:
                    # 获取每个详情页的url
                    url_list = response_json['result']['list']
                    for list in url_list:
                        info = list['master'] + list['pubtime']
                        detail_url = list['url']
                        try:
                            ex = redis_conn.sadd('gm_urls', detail_url)
                            if ex == 1:
                                get_detail_news(url=detail_url, keyword=keyword, id='gm' + str(count), info=info)
                                count += 1
                        except Exception as e:
                            print('后续页：' + detail_url + ',' + str(e))
                            continue
                else:
                    print('被封了！')
                    time.sleep(600)
            except Exception as e:
                print('后续页：' + url + ',' + str(e))
                continue

        print('【%s】关键词爬取完毕！' % keywords[keyword_num])
        fp2.write('【%s】关键词爬取完毕！\n' % keywords[keyword_num])
        fp2.close()
        keyword_num += 1
    print('【%s】内容爬取完毕！' % source)
