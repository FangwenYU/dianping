import scrapy
import json
from scrapy import Selector, Request
from dianping.items import DianpingShopIdItem, DianpingBannedUrlItem
import dianping.mysqldb as db


class ShopIdSpider(scrapy.Spider):

    name = 'shopid'

    # user_agent = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0)"}

    def __init__(self, city_id, category_id):
        self.city_id = city_id
        self.category_id = category_id

    def start_requests(self):
        page_url = 'http://www.dianping.com/search/category/{}/{}/{}p{}'

        for sub_category_id in db.get_shop_subcategory(self.category_id):
            for page in xrange(50):
                page_no = page + 1
                yield Request(page_url.format(self.city_id, self.category_id, sub_category_id, page_no),
                                  callback=self.parse_shop_id, dont_filter=True,
                                  meta={'shop_sub_category_id': sub_category_id})

    def parse_shop_id(self, response):
        if response.status == 403:
            print '403: %s' % response.url

            banned_url = DianpingBannedUrlItem()
            banned_url['spider_name'] = self.name
            banned_url['url'] = response.url
            banned_url['city_id'] = self.city_id
            banned_url['category_id'] = self.category_id

            yield banned_url
            # db.insert_banned_url(self.name, banned_url, self.city_id, self.category_id)

        else:
            data = Selector(response).xpath('//div[@id="shop-all-list"]/ul/li')
            sub_category_id = response.meta['shop_sub_category_id']
            for item in data:
                shop = DianpingShopIdItem()
                url = item.xpath('div[@class="pic"]/a/@href').extract()[0]
                shop_id = url.split('/')[-1]
                shop['shop_id'] = shop_id
                shop['city_id'] = self.city_id
                shop['category_id'] = self.category_id
                shop['sub_category_id'] = sub_category_id
                shop['shop_url'] = 'http://www.dianping.com/shop/{}'.format(shop_id)

                yield shop
