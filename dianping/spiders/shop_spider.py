# -*- coding: utf-8 -*-

from scrapy import Request
import dianping.mysqldb as db
from dianping.spiders.base_shop_spider import BaseShopSpider


class ShopSpider(BaseShopSpider):

    name = 'shop'

    def start_requests(self):
        for shop_url in db.get_shop(self.city_id, self.category_id):
            yield Request(shop_url, callback=self.parse_shop, dont_filter=True)
