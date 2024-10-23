import pyodbc


def store_in_sqlServer(item):
    conn = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=***;charset=cp936')
    cursor = conn.cursor()
    sql = "insert into *** " \
          "values ('%s','%s','%s','%s','%s','%s','%d')" % (
          item['title'], item['info'], item['content'], item['keyword'], item['url'],item['id'],1)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
    conn = None
    cursor = None

def store_in_text(item):
    fp = open('***.txt', 'a', encoding='utf-8')
    fp.write(item['title'] + '\n')
    fp.write(item['keyword'] + '\n')
    fp.write(item['info'] + '\n')
    fp.write(item['content'] + '\n')
    fp.close()