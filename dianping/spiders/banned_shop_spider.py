# -*- coding: utf-8 -*-

from scrapy import Request
import dianping.mysqldb as db
from dianping.spiders.base_shop_spider import BaseShopSpider

class BannedShopSpider(BaseShopSpider):

    name = 'banned_shop'

    def start_requests(self):
        for shop_url, city_id, category_id in db.get_banned_url('shop'):
            self.city_id = city_id
            self.category_id = category_id
            yield Request(shop_url, callback=self.parse_shop, dont_filter=True)
