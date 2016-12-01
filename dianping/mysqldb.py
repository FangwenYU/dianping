import mysql.connector
from scrapy.conf import settings

# http://dev.mysql.com/doc/connector-python/en/connector-python-examples.html


class MySQL(object):

    def __init__(self):

        self.mysql_config = {
            'user': settings['MYSQL_USER'],
            'password': settings['MYSQL_PASSWORD'],
            'host': settings['MYSQL_HOST'],
            'database': settings['MYSQL_DB'],
            'port': settings['MYSQL_PORT']
        }

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.connection.cursor(buffered=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return False


def get_shop(city_id, category_id):
    sql = "select shop_url from dianping_shop_id where city_id=%s and category_id=%s"
    data = [city_id, category_id]
    with MySQL() as db:
        cursor = db.cursor
        cursor.execute(sql, data)
        for shop in cursor:
            yield shop[0]

def get_shop_subcategory(category_id):
    sql = "select sub_category_id from dianping_shop_subcategory where category_id=%s"
    data = [category_id]
    with MySQL() as db:
        cursor = db.cursor
        cursor.execute(sql, data)
        for sub_category in cursor:
            yield sub_category[0]


def insert_banned_url(spider, url, city_id, category_id):
    sql = "insert into dianping_banned_url(spider_name, url, city_id, category_id) values(%s, %s, %s, %s)"
    data = [spider, url, city_id, category_id]
    with MySQL() as db:
        cursor = db.cursor
        cursor.execute(sql, data)


def get_banned_url(spider):
    sql = "select url, city_id, category_id from dianping_banned_url where spider_name=%s"
    data = [spider]
    with MySQL() as db:
        cursor = db.cursor
        cursor.execute(sql, data)
        for url in cursor:
            yield (url[0], url[1], url[2])