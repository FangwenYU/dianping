# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector, Request


class TestSpider(scrapy.Spider):

    name = 'test'

    start_urls = ['http://www.dianping.com/shop/1697902', 'http://www.dianping.com/shop/21279868',
                  'http://www.dianping.com/shop/2984299', 'http://www.dianping.com/shop/2775154']

    def parse(self, response):
        shop_id = response.url.split('/')[-1].strip()
        shop_url = response.url

        data = Selector(response).xpath('//div[@class="page-main"]')
        main = Selector(response).xpath('//div[@class="market-main"]')
        detail = Selector(response).xpath('//div[@class="market-detail"]')
        detail_other = Selector(response).xpath('//div[@class="market-detail-other Hide"]')

        navigator_div = data.xpath('div[@class="breadcrumb"]')

        location = []
        for loc in navigator_div.xpath('a'):
            location.append(loc.xpath('text()').extract()[0].strip())
        shop_navigation_path = '>'.join(location)

        print shop_navigation_path

        shop_name = main.xpath('h2[@class="market-name"]/text()').extract()[0].strip()

        print shop_name

        shop_address_info = detail.xpath('p')[0]
        shop_district = shop_address_info.xpath('a[@class="link-dk"]/text()').extract()[0].strip()

        print shop_district

        shop_address = ''.join([text.extract().strip() for text in shop_address_info.xpath('text()')])

        print shop_address

        shop_phone_1 = None
        shop_phone_2 = None
        shop_rank = None
        shop_taste_score = None
        shop_env_score = None
        shop_service_score = None
        shop_price = None
        shop_review = None


        for detail in detail_other.xpath('p'):
            title = detail.xpath('span[@class="title"]/text()').extract()[0].strip()
            if title.startswith(u'联系电话'):
                shop_phone_1 = ''.join([text.extract().strip() for text in detail.xpath('text()')])

            elif title.startswith(u'用户评级'):
                try:
                    shop_rank = detail.xpath('span')[1].xpath('@class').extract()[0].strip().strip('mid-rank-stars mid-str')[:2]
                    shop_rank = int(shop_rank)/10.0
                except:
                    pass
                shop_taste_score = detail.xpath('span')[2].xpath('text()').extract()[0].strip()
                shop_env_score = detail.xpath('span')[3].xpath('text()').extract()[0].strip()
                shop_service_score = detail.xpath('span')[4].xpath('text()').extract()[0].strip()

            elif title.startswith(u'人均消费'):
                shop_price = ''.join([text.extract().strip() for text in detail.xpath('text()')])

        print shop_phone_1
        print shop_rank
        print shop_taste_score, shop_env_score, shop_service_score, shop_price
