from selenium import webdriver
from time import sleep
from lxml import etree
from DetailGet import get_detail_news
# from redis import Redis

# 关键词
keywords = []
# id 计数
count = 0

fp = open(r'keywords_set.txt', 'r', encoding='utf-8')
keywords = fp.read().split(',')
keywords = list(set(keywords))
print('这一次有%d个关键词'%len(keywords))

keyword_num = 0

# 连接redis
# redis_conn = Redis(host='127.0.0.1',port=6379)

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('no-sandbox')
options.add_argument('--disable-gpu')
# 禁止加载图片
options.add_argument('--blink-setting=imagesEnable=false')

# 规避检测
options.add_experimental_option('excludeSwitches',['enable-automation'])

service = webdriver.ChromeService(executable_path=r'chromedriver.exe')

# 获取起始页
bro = webdriver.Chrome(options=options,service=service)
bro.get('https://www.cenews.com.cn/')

bro.find_element_by_class_name('el-input__inner').send_keys(keywords[keyword_num])
bro.find_element_by_class_name('el-icon-search').click()
sleep(2)
windows = bro.window_handles
bro.switch_to.window(windows[1])

# 获取到搜索页面
li_num = 0
n_count = 0
while keyword_num < len(keywords):
    page_text = etree.HTML(bro.page_source)
    li_list = page_text.xpath('//ul[@class="listBox"]/li')
    print(keywords[keyword_num])
    while li_num < len(li_list) and n_count <= 100:
        li_num = len(li_list)
        try:
            bro.find_element_by_class_name('morePage-text').click()
            sleep(2)
            page_text = etree.HTML(bro.page_source)
            li_list = page_text.xpath('//ul[@class="listBox"]/li')
            n_count += 1
        except:
            break
    # 这一页所有的新闻已加载
    for li in li_list:
        try:
            url = 'https://www.cenews.com.cn'+''.join(li.xpath('./a/@href')).lstrip('.')
            ex = redis_conn.sadd('cen_urls', url)
            if ex == 1:
                get_detail_news(url=url,keyword=keywords[keyword_num],id='cen'+str(count))
                count += 1
        except Exception as e:
            print(e)
            continue

    # 将li标签更新
    li_num = 0

    print('【%s】关键词爬取完毕！' % keywords[keyword_num])

    # 搜索下一个关键词
    keyword_num += 1
    if keyword_num < len(keywords):
        bro.find_element_by_xpath('//div[@class="el-input el-input-group el-input-group--append"]/input').clear()
        bro.find_element_by_xpath('//div[@class="el-input el-input-group el-input-group--append"]/input').send_keys(keywords[keyword_num])
        bro.find_element_by_xpath('//div[@class="el-input-group__append"]/button').click()
        sleep(2)
        # 关闭掉当前的页面
        new_windows = bro.window_handles
        bro.close()
        bro.switch_to.window(new_windows[2])

bro.quit()