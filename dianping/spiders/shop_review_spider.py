# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector, Request
from dianping.items import DianpingShopReviewItem
import dianping.mysqldb as db

class ShopReviewSpider(scrapy.Spider):

    name = 'shop_review'

    def __init__(self, city_id, category_id):
        self.city_id = city_id
        self.category_id = category_id

    def start_requests(self):
        for shop_url in db.get_shop(self.city_id, self.category_id):
            yield Request(shop_url, callback=self.parse_shop, dont_filter=True)

    def parse_shop(self, response):
        shop_id = response.url.split('/')[-1].strip()
        shop_url = response.url

        print shop_id, shop_url

        review_list = Selector(response).xpath('//li[@class="comment-item"]')

        if not review_list:
            return

        for review in review_list:
            user_info = review.xpath('p[@class="user-info"]')
            user_id = user_info.xpath('a/text()').extract()[0]
            user_url = 'www.dianping.com' + user_info.xpath('a/@href').extract()[0]

            user_shop_score = review.xpath('div[@class="content"]/p[@class="shop-info"]')
            shop_score = '|'.join(user_shop_score.xpath('span[@class="item"]/text()').extract())

            user_shop_review = review.xpath('div[@class="content"]/div[@class="info J-info-all Hide"]/p[@class="desc J-desc"]/text()').extract()
            if user_shop_review:
                shop_review = ''.join(user_shop_review)
            else:
                user_shop_review = review.xpath('div[@class="content"]/p[@class="desc"]/text()').extract()
                shop_review = ''.join(user_shop_review)

        item = DianpingShopReviewItem()
        item['shop_id'] = shop_id
        item['shop_url'] = shop_url
        item['user_id'] = user_id
        item['user_url'] = user_url
        item['shop_score'] = shop_score
        item['shop_review'] = shop_review

        yield item


