# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector, Request


class TestSpider(scrapy.Spider):

    name = 'test2'

    start_urls = ['http://www.dianping.com/shop/43628851', 'http://www.dianping.com/shop/19282518']

    def parse(self, response):
        shop_id = response.url.split('/')[-1].strip()
        shop_url = response.url

        data = Selector(response).xpath('//div[@class="page-main"]')
        main = Selector(response).xpath('//div[@class="market-main"]')
        detail = Selector(response).xpath('//div[@class="market-detail"]')
        detail_other = Selector(response).xpath('//div[@class="market-detail-other Hide"]')

        navigator_div = Selector(response).xpath('//div[@class="breadcrumb"]')

        location = []
        for loc in navigator_div.xpath('b/a/span'):
            location.append(loc.xpath('text()').extract()[0].strip())
        shop_navigation_path = '>'.join(location)

        print shop_navigation_path

        shop_name = Selector(response).xpath('//div[@class="shop-name"]/h1/text()').extract()[0].strip()

        print shop_name

        shop_district = Selector(response).xpath('//span[@class="region"]/text()').extract()[0].strip()

        print shop_district

        shop_address = Selector(response).xpath('//span[@itemprop="street-address"]/text()').extract()[0].strip()

        print shop_address

        shop_phone_1 = None
        shop_phone_2 = None
        shop_rank = Selector(response).xpath('//div[@class="comment-rst"]/span/@title').extract()[0].strip()
        shop_taste_score = None
        shop_env_score = None
        shop_service_score = None
        shop_price = Selector(response).xpath('//div[@class="comment-rst"]/dl/dd/text()').extract()[0].strip()
        shop_review = Selector(response).xpath('//div[@class="comment-rst"]/a/span/text()').extract()[0].strip()



        print shop_phone_1
        print shop_rank
        print shop_taste_score, shop_env_score, shop_service_score, shop_price, shop_review
