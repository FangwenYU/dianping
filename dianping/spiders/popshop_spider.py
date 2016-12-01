import scrapy
import json
from scrapy import Request
from dianping.items import DianpingPopShopItem


class PopShopSpider(scrapy.Spider):

    name = 'popshop'

    # start_urls = ['http://www.dianping.com/shoplist/all_344_10']
    # start_urls = ['http://www.dianping.com/mylist/ajax/shoprank?cityId=344&shopType=10&&rankType=3&categoryId=0']

    start_urls = ['http://www.dianping.com/mylist/ajax/shoprank?cityId=344&shopType=10&rankType=3&categoryId=0',  #Food
            # 'http://www.dianping.com/mylist/ajax/shoprank?cityId=344&shopType=10&rankType=1&categoryId=0',
            'http://www.dianping.com/mylist/ajax/shoprank?cityId=344&shopType=20&rankType=3&categoryId=0',  #Shopping
            'http://www.dianping.com/mylist/ajax/shoprank?cityId=344&shopType=45&rankType=3&categoryId=0',  #Sports
    ]

    # def start_requests(self):
    #     for url in self.urls:
    #         yield Request(url)

    def parse(self, response):
        result = json.loads(response.body)

        category_id = result['categoryId']
        city_id = result['cityId']

        for shop in result['shopBeans']:
            shop_item = DianpingPopShopItem()
            shop_item['city_id'] = city_id
            shop_item['shop_type'] = shop['shopType']
            shop_item['primary_tag'] = shop['primaryTag']
            shop_item['shop_id'] = shop['shopId']
            shop_item['shop_add_date'] = shop['addDate']
            shop_item['shop_group_id'] = shop['shopGroupId']
            shop_item['name'] = shop['fullName']
            shop_item['power'] = shop['power']
            shop_item['shop_power'] = shop['shopPower']
            shop_item['shop_power_title'] = shop['shopPowerTitle']
            shop_item['address']= shop['fullAdress']
            shop_item['avg_price'] = shop['avgPrice']
            shop_item['price_level'] = shop['priceLevel']
            shop_item['price_info'] = shop['priceInfo']
            shop_item['hits'] = shop['hits']
            shop_item['today_hits'] = shop['todayHits']
            shop_item['weekly_hits'] = shop['weeklyHits']
            shop_item['monthly_hits'] = shop['monthlyHits']
            shop_item['prev_weekly_hits'] = shop['prevWeeklyHits']
            shop_item['vote_total'] = shop['voteTotal']
            shop_item['main_category_id'] = shop['mainCategoryId']
            shop_item['main_category_name'] = shop['mainCategoryName']
            shop_item['region_id'] = shop['regionId']
            shop_item['main_region_id'] = shop['mainRegionId']
            shop_item['main_region_name'] = shop['mainRegionName']
            shop_item['phone_no'] = shop['phoneNo']
            shop_item['phone_no_2'] = shop['phoneNo2']
            shop_item['popularity'] = shop['popularity']
            shop_item['shop_taste_point'] = shop['refinedScore1']
            shop_item['shop_environment_point'] = shop['refinedScore2']
            shop_item['shop_service_point'] = shop['refinedScore3']
            shop_item['business_hour'] = shop['businessHours']
            shop_item['url'] = 'http://www.dianping.com/shop/{}'.format(shop['shopId'])
            shop_item['category_id'] = category_id

            yield shop_item
