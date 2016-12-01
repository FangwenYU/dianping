# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from dianping.items import DianpingShopItem, DianpingBannedUrlItem, DianpingErrorUrlItem

class BaseShopSpider(scrapy.Spider):

    # http://www.dianping.com/ajax/json/shop/wizard/getReviewListFPAjax?_nr_force=1457497905400&act=getreviewlist&shopId=559662&tab=all&order=

    # name = 'shop'

    # //span[@class="num"]

    # http://doc.scrapy.org/en/latest/topics/jobs.html

    # user_agent = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0)"}
    # Configure user agent in settings.py

    def __init__(self, city_id, category_id):
        self.city_id = city_id
        self.category_id = category_id

    def parse_shop(self, response):

        if response.status == 403:

            print '403: %s' % response.url

            self.logger.error('403: failed to crawl: {}'.format(response.url))

            banned_url = DianpingBannedUrlItem()
            banned_url['spider_name'] = self.name
            banned_url['url'] = response.url
            banned_url['city_id'] = self.city_id
            banned_url['category_id'] = self.category_id

            yield banned_url

        else:

            try:
                yield self.parse_shop_1(response)
            except:
                try:
                    yield self.parse_shop_2(response)
                except:
                    try:
                        yield self.parse_shop_3(response)
                    except:
                        self.logger.error('Failed to parse page: {}'.format(response.url))

                        error_url = DianpingErrorUrlItem()
                        error_url['spider_name'] = self.name
                        error_url['url'] = response.url
                        error_url['city_id'] = self.city_id
                        error_url['category_id'] = self.category_id

                        yield error_url

    def parse_shop_1(self, response):
        shop_id = response.url.split('/')[-1].strip()
        shop_url = response.url

        data = Selector(response).xpath('//div[@id="body"]')

        navigator_div = data.xpath('div/div[@class="breadcrumb"]')
        location = []
        for loc in navigator_div.xpath('a'):
            location.append(loc.xpath('text()').extract()[0].strip())
        shop_navigation_path = '>'.join(location)

        main_info = data.xpath('div/div[@class="main"]/div[@id="basic-info"]')
        shop_name = main_info.xpath('h1[@class="shop-name"]/text()').extract()[0].strip()

        brief_info = main_info.xpath('div[@class="brief-info"]/span')
        brief_info_item_len = len(brief_info)

        shop_rank = brief_info[0].xpath('@title').extract()[0] if brief_info_item_len > 0 else ''

        shop_review = brief_info[1].xpath('text()').extract()[0].strip() if brief_info_item_len > 1 else ''
        shop_price = brief_info[2].xpath('text()').extract()[0].strip() if brief_info_item_len > 2 else ''
        shop_taste_score = brief_info[3].xpath('text()').extract()[0].strip() if brief_info_item_len > 3 else ''
        shop_env_score = brief_info[4].xpath('text()').extract()[0].strip() if brief_info_item_len > 4 else ''
        shop_service_score = brief_info[5].xpath('text()').extract()[0].strip() if brief_info_item_len > 5 else ''

        # shop review could be None
        if shop_review.startswith(u'人均') or shop_review.startswith(u'消费'):
            shop_review, shop_price, shop_taste_score, shop_env_score, shop_service_score = \
                '', shop_review, shop_price, shop_taste_score, shop_env_score

        address_info = main_info.xpath('div[@class="expand-info address"]')
        district = address_info.xpath('a/span/text()').extract()
        shop_district = district[0].strip() if district and len(district) > 0 else ''
        shop_address = address_info.xpath('span[@class="item"]/text()').extract()[0].strip()

        shop_tel_info = main_info.xpath('p[@class="expand-info tel"]/span')
        shop_phone_len = len(shop_tel_info)

        shop_phone_1 = shop_tel_info[1].xpath('text()').extract()[0].strip() if shop_phone_len > 1 else ''
        shop_phone_2 = shop_tel_info[2].xpath('text()').extract()[0].strip() if shop_phone_len > 2 else ''

        shop = DianpingShopItem()
        shop['shop_id'] = shop_id
        shop['shop_url'] = shop_url
        shop['shop_navigation_path'] = shop_navigation_path
        shop['shop_name'] = shop_name
        shop['shop_rank'] = shop_rank
        shop['shop_review'] = shop_review
        shop['shop_price'] = shop_price
        shop['shop_taste_score'] = shop_taste_score
        shop['shop_env_score'] = shop_env_score
        shop['shop_service_score'] = shop_service_score
        shop['shop_district'] = shop_district
        shop['shop_address'] = shop_address
        shop['shop_phone_1'] = shop_phone_1
        shop['shop_phone_2'] = shop_phone_2
        shop['city_id'] = self.city_id
        shop['category_id'] = self.category_id

        return shop

    def parse_shop_2(self, response):
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
        shop_name = main.xpath('h2[@class="market-name"]/text()').extract()[0].strip()

        shop_address_info = detail.xpath('p')[0]
        shop_district = shop_address_info.xpath('a[@class="link-dk"]/text()').extract()[0].strip()
        shop_address = ''.join([text.extract().strip() for text in shop_address_info.xpath('text()')])
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

        shop = DianpingShopItem()
        shop['shop_id'] = shop_id
        shop['shop_url'] = shop_url
        shop['shop_navigation_path'] = shop_navigation_path
        shop['shop_name'] = shop_name
        shop['shop_rank'] = shop_rank
        shop['shop_review'] = shop_review
        shop['shop_price'] = shop_price
        shop['shop_taste_score'] = shop_taste_score
        shop['shop_env_score'] = shop_env_score
        shop['shop_service_score'] = shop_service_score
        shop['shop_district'] = shop_district
        shop['shop_address'] = shop_address
        shop['shop_phone_1'] = shop_phone_1
        shop['shop_phone_2'] = shop_phone_2
        shop['city_id'] = self.city_id
        shop['category_id'] = self.category_id

        return shop

    def parse_shop_3(self, response):
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
        shop_name = main.xpath('h2[@class="market-name"]/text()').extract()[0].strip()

        shop_address_info = detail.xpath('p')[0]
        shop_district = shop_address_info.xpath('a[@class="link-dk"]/text()').extract()[0].strip()

        shop_address = ''.join([text.extract().strip() for text in shop_address_info.xpath('text()')])

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

        shop = DianpingShopItem()
        shop['shop_id'] = shop_id
        shop['shop_url'] = shop_url
        shop['shop_navigation_path'] = shop_navigation_path
        shop['shop_name'] = shop_name
        shop['shop_rank'] = shop_rank
        shop['shop_review'] = shop_review
        shop['shop_price'] = shop_price
        shop['shop_taste_score'] = shop_taste_score
        shop['shop_env_score'] = shop_env_score
        shop['shop_service_score'] = shop_service_score
        shop['shop_district'] = shop_district
        shop['shop_address'] = shop_address
        shop['shop_phone_1'] = shop_phone_1
        shop['shop_phone_2'] = shop_phone_2
        shop['city_id'] = self.city_id
        shop['category_id'] = self.category_id

        return shop
