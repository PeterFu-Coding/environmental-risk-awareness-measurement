from lxml import etree
import requests
from time import sleep
import urllib3
import store
import textProcess.stringProcessor as sp

def get_detail_news(url,keyword,id):
    headers = {
        "User-Agent": "***"
    }
    json_url = 'https://cmsapi.cenews.com.cn/api/getArticle?'+url.split('?')[-1]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url=json_url,headers=headers,verify=False)

    sleep(1)
    response.encoding = response.apparent_encoding
    response_json = response.json()
    page_text = etree.HTML(response_json['content'])
    title = response_json['title']
    info = response_json['source']+'|'+response_json['publishTime']
    content = ''.join(page_text.xpath('//p/text() | //p//text() | //section//text()'))

    # 文本初步处理
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

