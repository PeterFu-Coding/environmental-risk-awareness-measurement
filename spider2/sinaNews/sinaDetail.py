from lxml import etree
import requests
import store
from time import sleep
import textProcess.stringProcessor as sp


def get_detail_news(url,keyword,id):
    headers = {
        "User-Agent": "***"
    }
    response = requests.get(url=url,headers=headers,verify=False)
    sleep(0.5)
    response.encoding = response.apparent_encoding
    page_text = etree.HTML(response.text)
    title = ''.join(page_text.xpath('//h1[@class="main-title"]/text() | //div[@class="article-header clearfix"]/h1/text()'))
    info = ' '.join(page_text.xpath('//div[@class="date-source"]//text() | //p[@class="source-time"]//text()'))
    content = ''.join(page_text.xpath('//div[@class="article"]/p//text() | //div[@class="article-body main-body"]/p//text()'))

    content = sp.content_clr(content)

    item={
        'title':title,
        'info':info,
        'content':content,
        'url':url,
        'keyword':keyword,
        'id':id
    }

    store.store_in_sqlServer(item)
    store.store_in_text(item)
