import random
import time
import requests
import urllib3
import textProcess.stringProcessor as sp
from lxml import etree
import GMStore


def get_detail_news(url, keyword, id, info):
    headers = {
        "user-agent": '***'
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    s = requests.session()
    s.keep_alive = False
    rand = random.randint(0, 10)
    response = requests.get(url=url, headers=headers, verify=False)

    time.sleep(rand)

    response.encoding = 'utf-8'
    page_text = etree.HTML(response.text)
    title = ''.join(page_text.xpath("//div[@class='m-title-box']/h1//text() | //div[@class='text_c']/h1//text() | //h1[@id='articleTitle']//text()"))
    content = ''.join(page_text.xpath(
        "//div[@id='article_inbox']/div[@class='u-mainText']/p//text() | //div[@class='articleContent']/p//text() | "
        "//div[@class='c_c']//text() | //div[@id = 'contentMain']//text()"))

    content = sp.content_clr(content)

    item = {
        'title': title,
        'info': info,
        'content': content,
        'url': url,
        'keyword': keyword,
        'id': id
    }

    response.close()
    GMStore.store_in_sqlServer(item)
    GMStore.store_in_text(item)
