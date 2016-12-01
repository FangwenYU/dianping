# -*- coding: utf-8 -*-

import mysql.connector
from scrapy.conf import settings
import abc
from dianping.tables import DBSession, DianpingShop, DianpingShopId, DianpingPopShop, DianpingBannedUrl, DianpingErrorUrl, DianpingShopReview
from dianping.items import DianpingShopIdItem, DianpingShopItem, DianpingPopShopItem, DianpingBannedUrlItem, DianpingErrorUrlItem, DianpingShopReviewItem


class MySQLPipeline(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.mysql_config = {
            'user': settings['MYSQL_USER'],
            'password': settings['MYSQL_PASSWORD'],
            'host': settings['MYSQL_HOST'],
            'database': settings['MYSQL_DB'],
            'port': settings['MYSQL_PORT']
        }

    def open_spider(self, spider):
        self.session = DBSession()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item

    @abc.abstractmethod
    def insert_item(self, shop_item):
        """to be override in subclass
        :type item: scrapy.Item
        """


class DianpingPipeline(MySQLPipeline):

    def insert_item(self, shop_item):

        shop = None

        if isinstance(shop_item, DianpingShopItem):
            shop = DianpingShop(
                shop_id=shop_item['shop_id'],
                shop_url=shop_item['shop_url'],
                shop_navigation_path=shop_item['shop_navigation_path'],
                shop_name=shop_item['shop_name'],
                shop_rank=shop_item['shop_rank'],
                shop_review=shop_item['shop_review'],
                shop_price=shop_item['shop_price'],
                shop_taste_score=shop_item['shop_taste_score'],
                shop_env_score=shop_item['shop_env_score'],
                shop_service_score=shop_item['shop_service_score'],
                shop_district=shop_item['shop_district'],
                shop_address=shop_item['shop_address'],
                shop_phone_1=shop_item['shop_phone_1'],
                shop_phone_2=shop_item['shop_phone_2'],
                city_id = shop_item['city_id'],
                category_id = shop_item['category_id']
            )
        elif isinstance(shop_item, DianpingShopIdItem):
            shop = DianpingShopId(
                shop_id = shop_item['shop_id'],
                city_id = shop_item['city_id'],
                category_id = shop_item['category_id'],
                sub_category_id = shop_item['sub_category_id'],
                shop_url = shop_item['shop_url']
            )
        elif isinstance(shop_item, DianpingPopShopItem):
            shop = DianpingPopShop(
                city_id=shop_item['city_id'],
                shop_type=shop_item['shop_type'],
                primary_tag=shop_item['primary_tag'],
                shop_id=shop_item['shop_id'],
                shop_add_date=shop_item['shop_add_date'],
                shop_group_id=shop_item['shop_group_id'],
                name=shop_item['name'],
                power=shop_item['power'],
                shop_power=shop_item['shop_power'],
                shop_power_title=shop_item['shop_power_title'],
                address=shop_item['address'],
                avg_price=shop_item['avg_price'],
                price_level=shop_item['price_level'],
                price_info=shop_item['price_info'],
                hits=shop_item['hits'],
                today_hits=shop_item['today_hits'],
                weekly_hits=shop_item['weekly_hits'],
                monthly_hits=shop_item['monthly_hits'],
                prev_weekly_hits=shop_item['prev_weekly_hits'],
                vote_total=shop_item['vote_total'],
                main_category_id=shop_item['main_category_id'],
                main_category_name=shop_item['main_category_name'],
                region_id=shop_item['region_id'],
                main_region_id=shop_item['main_region_id'],
                main_region_name=shop_item['main_region_name'],
                phone_no=shop_item['phone_no'],
                phone_no_2=shop_item['phone_no_2'],
                popularity=shop_item['popularity'],
                shop_taste_point=shop_item['shop_taste_point'],
                shop_environment_point=shop_item['shop_environment_point'],
                shop_service_point=shop_item['shop_service_point'],
                business_hour=shop_item['business_hour'],
                url=shop_item['url'],
                category_id=shop_item['category_id']
            )
        elif isinstance(shop_item, DianpingShopReviewItem):
            shop = DianpingShopReview(
                ship_id = shop_item['shop_id'],
                shop_url = shop_item['shop_url'],
                user_id = shop_item['user_id'],
                user_url = shop_item['user_url'],
                shop_score = shop_item['shop_score'],
                shop_review = shop_item['shop_review']
            )

        if shop:
            try:
                self.session.add(shop)
                self.session.commit()  # in case losing connection to database due to long time processing
            except mysql.connector.errors.IntegrityError:
                pass


class DianpingBannedUrlPipeline(MySQLPipeline):

    def insert_item(self, item):
        if isinstance(item, DianpingBannedUrlItem):
            banned_url = DianpingBannedUrl(
                spider_name=item['spider_name'],
                url=item['url'],
                city_id=item['city_id'],
                category_id=item['category_id'])
            try:
                self.session.add(banned_url)
                self.session.commit()
            except mysql.connector.errors.IntegrityError:
                pass



class DianpingErrorUrlPipeline(MySQLPipeline):

    def insert_item(self, item):
        if isinstance(item, DianpingErrorUrlItem):
            banned_url = DianpingErrorUrl(
                spider_name=item['spider_name'],
                url=item['url'],
                city_id=item['city_id'],
                category_id=item['category_id'])
            try:
                self.session.add(banned_url)
                self.session.commit()
            except mysql.connector.errors.IntegrityError:
                pass
