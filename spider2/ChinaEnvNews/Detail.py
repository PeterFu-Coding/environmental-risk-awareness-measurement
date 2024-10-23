from lxml import etree
import store
from time import sleep
from selenium import webdriver
import textProcess.stringProcessor as sp

def get_detail_news(url,keyword,id):
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-setting=imagesEnable=false')
    # 规避检测
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('--disable-gpu')
    web = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    web.get(url)
    sleep(3)
    page_text = etree.HTML(web.page_source)

    title = ''.join(page_text.xpath('//div[@class="messBox el-row"]/h5/text()'))
    info = ' '.join(page_text.xpath('//div[@class="messBox el-row"]/p//text()'))
    content = ''.join(page_text.xpath('//div[@class="artContent el-row"]/p//text()'))

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
    web.close()
