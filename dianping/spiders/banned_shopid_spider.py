import scrapy
from scrapy import Selector, Request
from dianping.items import DianpingShopIdItem, DianpingBannedUrlItem
import dianping.mysqldb as db

class BannedShopIdSpider(scrapy.Spider):

    name = 'banned_shopid'

    # user_agent = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0)"}

    def start_requests(self):
        for url, city_id, category_id in db.get_banned_url('shopid'):
            yield Request(url,callback=self.parse_shop_id, dont_filter=True,
                          meta={'city_id':city_id, 'category_id':category_id})

    def parse_shop_id(self, response):
        city_id = response.meta['city_id']
        category_id = response.meta['category_id']
        if response.status == 403:

            print '403: %s' % response.url

            banned_url = DianpingBannedUrlItem()
            banned_url['spider_name'] = self.name
            banned_url['url'] = response.url
            banned_url['city_id'] = city_id
            banned_url['category_id'] = category_id

            yield banned_url
            # db.insert_banned_url(self.name, banned_url, city_id, category_id)
        else:
            data = Selector(response).xpath('//div[@id="shop-all-list"]/ul/li')
            sub_category_id = response.url.split('/')[-1].split('p')[0]

            for item in data:
                shop = DianpingShopIdItem()
                url = item.xpath('div[@class="pic"]/a/@href').extract()[0]
                shop_id = url.split('/')[-1]
                shop['shop_id'] = shop_id
                shop['city_id'] = city_id
                shop['category_id'] = category_id
                shop['sub_category_id'] = sub_category_id
                shop['shop_url'] = 'http://www.dianping.com/shop/{}'.format(shop_id)

                yield shop
