# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector, Request


class CityIdSpider(scrapy.Spider):

    name = 'city_id'

    start_urls = ['http://www.dianping.com/citylist/citylist?citypage=1']

    def parse(self, response):

        data = Selector(response).xpath('//dd/a/@href').extract()

        for city in data:
            # print city
            city_life_url = 'http://www.dianping.com{}/life'.format(city)
            yield Request(url=city_life_url, callback=self.parse_city_life, meta={'city':city})

            city_food_url = 'http://www.dianping.com{}/food'.format(city)
            yield Request(url=city_food_url, callback=self.parse_city_food, meta={'city':city})


    def parse_city_life(self, response):
        city = response.meta['city'].strip('/')
        # print "city:", city
        data = Selector(response).xpath('//div[@class="hd"]/h1/span/a/text()').extract()[0].strip()
        data = data.strip(u'家')
        print u'{},{},{}'.format('life', city, data)
        # print data
        # print 'life', city, data

    def parse_city_food(self, response):
        city = response.meta['city'].strip('/')
        data = Selector(response).xpath('//div[@class="block popular-nav"]/div[@class="block-title"]/text()').extract()[0].strip()
        data = data.strip(u'共').strip(u'家餐厅')
        # print data
        print '{},{},{}'.format('food', city, data)


        # main = Selector(response).xpath('//div[@class="market-main"]')
        # detail = Selector(response).xpath('//div[@class="market-detail"]')
        # detail_other = Selector(response).xpath('//div[@class="market-detail-other Hide"]')
        #
        # # navigator_div = data.xpath('div[@class="breadcrumb"]')
        #
        # location = []
        # for loc in navigator_div.xpath('a'):
        #     location.append(loc.xpath('text()').extract()[0].strip())
        # shop_navigation_path = '>'.join(location)
        #
        # print shop_navigation_path
        #
        # shop_name = main.xpath('h2[@class="market-name"]/text()').extract()[0].strip()
        #
        # print shop_name
        #
        # shop_address_info = detail.xpath('p')[0]
        # shop_district = shop_address_info.xpath('a[@class="link-dk"]/text()').extract()[0].strip()
        #
        # print shop_district
        #
        # shop_address = ''.join([text.extract().strip() for text in shop_address_info.xpath('text()')])
        #
        # print shop_address
        #
        # shop_phone_1 = None
        # shop_phone_2 = None
        # shop_rank = None
        # shop_taste_score = None
        # shop_env_score = None
        # shop_service_score = None
        # shop_price = None
        # shop_review = None
        #
        #
        # for detail in detail_other.xpath('p'):
        #     title = detail.xpath('span[@class="title"]/text()').extract()[0].strip()
        #     if title.startswith(u'联系电话'):
        #         shop_phone_1 = ''.join([text.extract().strip() for text in detail.xpath('text()')])
        #
        #     elif title.startswith(u'用户评级'):
        #         try:
        #             shop_rank = detail.xpath('span')[1].xpath('@class').extract()[0].strip().strip('mid-rank-stars mid-str')[:2]
        #             shop_rank = int(shop_rank)/10.0
        #         except:
        #             pass
        #         shop_taste_score = detail.xpath('span')[2].xpath('text()').extract()[0].strip()
        #         shop_env_score = detail.xpath('span')[3].xpath('text()').extract()[0].strip()
        #         shop_service_score = detail.xpath('span')[4].xpath('text()').extract()[0].strip()
        #
        #     elif title.startswith(u'人均消费'):
        #         shop_price = ''.join([text.extract().strip() for text in detail.xpath('text()')])
        #
        # print shop_phone_1
        # print shop_rank
        # print shop_taste_score, shop_env_score, shop_service_score, shop_price
