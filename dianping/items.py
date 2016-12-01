# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DianpingPopShopItem(Item):
    city_id = Field()
    shop_type = Field()
    primary_tag = Field()
    shop_id = Field()
    shop_add_date = Field()
    shop_group_id = Field()
    name = Field()
    power = Field()
    shop_power = Field()
    shop_power_title = Field()
    address = Field()
    avg_price = Field()
    price_level = Field()
    price_info = Field()
    hits = Field()
    today_hits = Field()
    weekly_hits = Field()
    monthly_hits = Field()
    prev_weekly_hits = Field()
    vote_total = Field()
    main_category_id = Field()
    main_category_name = Field()
    region_id = Field()
    main_region_id = Field()
    main_region_name = Field()
    phone_no = Field()
    phone_no_2 = Field()
    popularity = Field()
    shop_taste_point = Field()
    shop_environment_point = Field()
    shop_service_point = Field()
    business_hour = Field()
    url = Field()
    category_id = Field()


class DianpingShopItem(Item):
    shop_id = Field()
    shop_url = Field()
    shop_navigation_path = Field()
    shop_name = Field()
    shop_rank = Field()
    shop_review = Field()
    shop_price = Field()
    shop_taste_score = Field()
    shop_env_score = Field()
    shop_service_score = Field()
    shop_district = Field()
    shop_address = Field()
    shop_phone_1 = Field()
    shop_phone_2 = Field()
    city_id = Field()
    category_id = Field()


class DianpingShopIdItem(Item):
    shop_id = Field()
    city_id = Field()
    category_id = Field()
    sub_category_id = Field()
    shop_url = Field()


class DianpingBannedUrlItem(Item):
    spider_name = Field()
    url = Field()
    city_id = Field()
    category_id = Field()


class DianpingErrorUrlItem(Item):
    spider_name = Field()
    url = Field()
    city_id = Field()
    category_id = Field()


class DianpingShopReviewItem(Item):
    shop_id = Field()
    shop_url = Field()
    user_id = Field()
    user_url = Field()
    shop_score = Field()
    shop_review = Field()

