# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pyodbc
from itemadapter import ItemAdapter


class XinhuaproPipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pyodbc.connect('DRIVER={sql server};server=127.0.0.1\SQLEXPRESS;database=***;charset=cp936')
        print("SQL Server连接成功！")

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        sql = "insert into *** " \
              "values ('%s','%s','%s','%s','%s','%s','%d')" % (
              item['title'], item['info'], item['content'], item['keyword'], item['url'],
              item['id'], 1)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.conn = None
        self.cursor = None


class XinhuaProPipelineToText:
    fp = None

    def open_spider(self, spider):
        self.fp = open('***.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(item['title'] + '\n')
        self.fp.write(item['keyword'] + '\n')
        self.fp.write(item['info'] + '\n')
        self.fp.write(item['content'] + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()
