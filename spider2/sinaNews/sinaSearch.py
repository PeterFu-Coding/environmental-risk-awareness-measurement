from selenium import webdriver
from time import sleep
from lxml import etree
from sinaDetail import get_detail_news
# from redis import Redis
import urllib3

# 关键词
keywords = []
fp = open('keywords.txt', 'r', encoding='utf-8')
keyword_list = fp.read().split(',')
for keyword in keyword_list:
    keywords.append(keyword)
keywords = list(set(keywords))

keyword_num = 0
# 编写id计数
id = 0

# 连接redis
# redis_conn = Redis(host='127.0.0.1',port=6379)

# options = webdriver.ChromeOptions()
options = webdriver.FirefoxOptions()

# options.add_argument('headless')
# options.add_argument('no-sandbox')
options.add_argument('--disable-gpu')
# 禁止加载图片
# options.add_argument('--blink-setting=imagesEnable=false')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 规避检测
# options.add_experimental_option('excludeSwitches',['enable-automation'])
profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False) #关闭自动化提示
profile.update_preferences()    #更新设置

options.profile = profile

service = webdriver.FirefoxService(executable_path=r'geckodriver.exe')


# 获取起始页
bro = webdriver.Firefox(service=service,options=options)
bro.get('https://search.sina.com.cn/news')

bro.find_element_by_class_name('ipt-01').send_keys(keywords[keyword_num])
bro.find_element_by_class_name('ipt-submit').click()
sleep(3)
# 登录
bro.find_element_by_xpath('//a[@class="login-button"]/span').click()
sleep(3)
bro.find_element_by_xpath('//li[@class="ndrelativewrap"]/input').send_keys('***')
bro.find_element_by_xpath('//ul[@class="loginformlist"]/li[3]/input').send_keys('***')
bro.find_element_by_class_name('login_btn').click()
# 要输入验证码，等待时间需要适当延长
sleep(30)
# 登录之后会重新跳转到首页，需要重新进行搜索
bro.find_element_by_class_name('ipt-01').send_keys(keywords[keyword_num])
bro.find_element_by_class_name('ipt-submit').click()
sleep(3)

# 获取到搜索页面
page_text = etree.HTML(bro.page_source)

while keyword_num < len(keywords):
    page_text = etree.HTML(bro.page_source)
    while ''.join(page_text.xpath('//div[@class="pagebox"]/a[last()]/@title')) == '下一页':
        div_list = page_text.xpath('//div[@class="box-result clearfix"]')
        for div in div_list:
            try:
                href = div.xpath('./h2/a/@href | ./div/h2/a/@href')[0]
                ex = redis_conn.sadd('sina_urls', href)
                if ex == 1:
                    get_detail_news(url=href, keyword=keywords[keyword_num],id='sina'+str(id))
                    id += 1
            except Exception as e:
                print(e)
                continue
        bro.find_element_by_xpath('//div[@class="pagebox"]/a[last()]').click()
        sleep(2)
        page_text = etree.HTML(bro.page_source)


    # 最后一页的数据
    div_list = page_text.xpath('//div[@class="box-result clearfix"]')
    for div in div_list:
        try:
            href = div.xpath('./h2/a/@href | ./div/h2/a/@href')[0]
            ex = redis_conn.sadd('sina_urls', href)
            if ex == 1:
                get_detail_news(url=href, keyword=keywords[keyword_num],id='sina'+str(id))
                id += 1
        except:
            continue

    print('【%s】关键词爬取完毕！'%keywords[keyword_num])

    # 搜索下一个关键词
    keyword_num += 1
    if keyword_num < len(keywords):
        bro.find_element_by_class_name('ipt-02').clear()
        bro.find_element_by_class_name('ipt-02').send_keys(keywords[keyword_num])
        bro.find_element_by_class_name('ipt-03').click()
        sleep(2)

bro.close()